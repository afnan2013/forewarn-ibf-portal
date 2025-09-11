from django.urls import path
from . import views

# Dashboard URLs  
# These handle dashboard data and analytics

app_name = 'dashboard'

urlpatterns = [
    # Dashboard endpoints
    path('stats/', views.dashboard_stats, name='stats'),
    path('overview/', views.dashboard_overview, name='overview'),
]
