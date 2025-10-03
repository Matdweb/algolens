from django.test import TestCase
from .algorithms import gen_random_list, bubble_sort
from .benchmark import run_benchmark

class BenchmarkTest(TestCase):
    def test_bubble_small(self):
        results = run_benchmark(bubble_sort, gen_random_list, sizes=[10, 50], repeats=2, max_total_seconds=5.0)
        self.assertTrue(len(results) >= 1)
        self.assertIn('avg', results[0])
