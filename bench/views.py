# bench/views.py (top imports snippet)
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import math
import json
import plotly.graph_objs as go

from .algorithms import (gen_random_list, bubble_sort, merge_sort, quick_sort, linear_search, binary_search)
from .benchmark import run_benchmark
from .models import Benchmark

ALGO_CHOICES = [
    ('bubble', 'Bubble sort (O(n^2))'),
    ('merge', 'Merge sort (O(n log n))'),
    ('quick', 'Quick sort (avg O(n log n))'),
    ('linear', 'Linear search (O(n))'),
    ('binary', 'Binary search (O(log n))'),  # will use sorted 
    ('custom', 'Custom Code')
]

class RunForm(forms.Form):
    algorithm = forms.ChoiceField(choices=ALGO_CHOICES)
    sizes = forms.CharField(initial='100,500,1000', help_text='Comma-separated sizes')
    repeats = forms.IntegerField(initial=3, min_value=1, max_value=10)
    custom_code = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 45,
            'placeholder': 'Define your function:\ndef custom_algo(arr):\n    # Your code here\n',
            'style': 'font-family: monospace; background: none; color: #0f0;',
        }),
        required=False,
        help_text='Define a function def custom_algo(arr): ...',
        initial='def custom_algo(arr):\n    # Your code here\n'
    )


def run_view(request):
    saved = False
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            alg = form.cleaned_data['algorithm']
            sizes = [int(s.strip()) for s in form.cleaned_data['sizes'].split(',') if s.strip().isdigit()]
            repeats = form.cleaned_data['repeats']

            # map to functions + generator(fn) and theory designation
            if alg == 'bubble':
                func = bubble_sort
                gen = gen_random_list
                theory = lambda n: n**2
                theory_label = 'O(n^2)'
            elif alg == 'merge':
                func = merge_sort
                gen = gen_random_list
                theory = lambda n: n * math.log(n, 2) if n > 0 else 0
                theory_label = 'O(n log n)'
            elif alg == 'quick':
                func = quick_sort
                gen = gen_random_list
                theory = lambda n: n * math.log(n, 2) if n > 0 else 0
                theory_label = 'O(n log n)'
            elif alg == 'linear':
                func = lambda arr: linear_search(arr, -1)  # worst-case target not found
                gen = gen_random_list
                theory = lambda n: n
                theory_label = 'O(n)'
            elif alg == 'binary':
                func = lambda arr: binary_search(sorted(arr), -1)
                gen = gen_random_list
                theory = lambda n: math.log(n, 2) if n > 0 else 0
                theory_label = 'O(log n)'
            elif alg == 'custom':
                code = form.cleaned_data['custom_code']
                # minimal sanitization: disallow imports and obvious system calls
                forbidden = ['import', 'os', 'sys', 'subprocess', 'open', 'exec', 'eval']
                if any(word in code for word in forbidden):
                    return render(request, 'bench/run.html', {
                        'form': form,
                        'error': 'Unsafe code detected: forbidden keywords.'
                    })

                # Provide a very small, safe set of builtins so user code can use print(), len(), etc.
                safe_builtins = {
                    'print': print,
                    'len': len,
                    'range': range,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'enumerate': enumerate,
                    'abs': abs,
                    'sorted': sorted,
                }

                local_env = {}
                try:
                    # Exec with restricted builtins to allow harmless helpers like print()
                    exec(code, {'__builtins__': safe_builtins}, local_env)
                    func = local_env.get('custom_algo')
                    if not callable(func):
                        return render(request, 'bench/run.html', {
                            'form': form,
                            'error': 'You must define a function named custom_algo(arr).'
                        })
                    gen = gen_random_list
                    theory = lambda n: n  # default placeholder
                    theory_label = 'Custom'
                except Exception as e:
                    return render(request, 'bench/run.html', {
                        'form': form,
                        'error': f'Code failed to compile: {e}'
                    })
            else:
                return render(request, 'bench/run.html', {'form': form, 'error': 'Unknown algorithm'})

            # cap sizes for heavy algorithms (safe defaults)
            safe_sizes = []
            for n in sizes:
                if alg == 'bubble' and n > 5000:
                    safe_sizes.append(5000)
                else:
                    safe_sizes.append(n)

            results = run_benchmark(func, gen, safe_sizes, repeats=repeats, gen_kwargs=None, max_total_seconds=30.0)

            ns = [r['n'] for r in results]
            avgs = [r.get('avg', 0) for r in results]

            # Plotly figure (same as before)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ns, y=avgs, mode='lines+markers', name='Measured (avg)'))

            if ns and any(theory(n) for n in ns):
                theory_vals = [theory(n) for n in ns]
                if theory_vals[0] == 0:
                    scale = 1.0
                else:
                    scale = avgs[0] / theory_vals[0] if theory_vals[0] else 1.0
                scaled = [scale * v for v in theory_vals]
                fig.add_trace(go.Scatter(x=ns, y=scaled, mode='lines', name=theory_label, line=dict(dash='dash')))

            fig.update_layout(
                title=f'Benchmark: {dict(ALGO_CHOICES)[alg]}', 
                xaxis_title='n (input size)',
                yaxis_title='time (seconds, avg)',
                paper_bgcolor='#000',
                plot_bgcolor='#000',
                font=dict(family='Courier New, monospace', color='#0f0', size=14),
                xaxis=dict(color='#0f0', gridcolor='#0a0', zerolinecolor='#0f0'),
                yaxis=dict(color='#0f0', gridcolor='#0a0', zerolinecolor='#0f0'),
                legend=dict(font=dict(color='#0f0')),
            )
            for trace in fig.data:
                trace.line.color = '#0f0'
                trace.marker.color = '#0f0'

            plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

            # Save benchmark for authenticated users
            if request.user.is_authenticated:
                try:
                    Benchmark.objects.create(
                        user=request.user,
                        algorithm=dict(ALGO_CHOICES)[alg],
                        sizes=','.join(map(str, ns)),
                        repeats=repeats,
                        results=results
                    )
                    saved = True
                except Exception as e:
                    # don't break the view if save fails; just continue
                    print("Failed saving benchmark:", e)

            return render(request, 'bench/result.html', {
                'plot_div': plot_div,
                'results': results,
                'algorithm': dict(ALGO_CHOICES)[alg], # need a fix here for 'custom'
                'saved': saved
            })
    else:
        form = RunForm()

    return render(request, 'bench/run.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # log the new user in
            return redirect('bench:run')
    else:
        form = UserCreationForm()
    return render(request, 'bench/signup.html', {'form': form})


@login_required
def history_view(request):
    benches = Benchmark.objects.filter(user=request.user)
    # Prepare pretty JSON for display
    benches_data = []
    import json
    for b in benches:
        # results might be Python-object (JSONField), convert to pretty JSON
        pretty = json.dumps(b.results, indent=2) if b.results is not None else "{}"
        benches_data.append({
            'id': b.id,
            'algorithm': b.algorithm,
            'sizes': b.sizes,
            'repeats': b.repeats,
            'created_at': b.created_at,
            'results_pretty': pretty
        })
    return render(request, 'bench/history.html', {'benches': benches_data})
