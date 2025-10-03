# bench/benchmark.py
import time
import statistics
from typing import Callable, List, Dict

def run_benchmark(func: Callable, gen_func: Callable, sizes: List[int],
                  repeats: int = 3, gen_kwargs: dict = None, max_total_seconds: float = 30.0):
    """
    func: algorithm function that accepts a generated input (list or similar)
    gen_func: function to create input for given n (e.g., gen_random_list)
    sizes: list of input sizes (ints)
    repeats: how many measurements per n
    gen_kwargs: optional kwargs for generator
    Returns: list of dicts with n, times, avg, median
    """
    gen_kwargs = gen_kwargs or {}
    results = []
    total_time = 0.0

    for n in sizes:
        times = []
        for _ in range(max(1, repeats)):
            data = gen_func(n, **gen_kwargs)
            # make sure func will not mutate the generator's return (we copy if it's a list)
            if isinstance(data, list):
                data_for_run = data.copy()
            else:
                data_for_run = data

            start = time.perf_counter()
            # execute algorithm
            _ = func(data_for_run)
            end = time.perf_counter()
            elapsed = end - start
            times.append(elapsed)
            total_time += elapsed
            if total_time > max_total_seconds:
                # prevent runaway long benchmarks
                return results + [{
                    "n": n,
                    "times": times,
                    "avg": statistics.mean(times),
                    "median": statistics.median(times),
                    "note": "stopped: time limit reached"
                }]

        results.append({
            "n": n,
            "times": times,
            "avg": statistics.mean(times),
            "median": statistics.median(times)
        })
    return results
