from django.contrib import admin
from .models import Benchmark

@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ('algorithm', 'user', 'created_at', 'repeats')
    search_fields = ('algorithm', 'user__username')
    list_filter = ('algorithm', 'created_at')
    readonly_fields = ('created_at',)
    