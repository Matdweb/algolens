from django.db import models
from django.conf import settings

class Benchmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='benchmarks')
    algorithm = models.CharField(max_length=100)
    sizes = models.CharField(max_length=200)   # store as comma-separated string (easy to display)
    repeats = models.IntegerField(default=1)
    results = models.JSONField()                # requires Django 3.1+. If you use older Django, see fallback below.
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.algorithm} — {self.user} — {self.created_at:%Y-%m-%d %H:%M}"
