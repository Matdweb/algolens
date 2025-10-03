# bench/urls.py
from django.urls import path
from . import views

app_name = 'bench'

urlpatterns = [
    path('', views.run_view, name='run'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
]
