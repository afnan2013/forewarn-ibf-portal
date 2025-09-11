from django.urls import path
from . import views

# User management URLs
# These handle user CRUD operations

app_name = 'users'

urlpatterns = [
    # User endpoints
    path('profile/', views.user_profile, name='profile'),
    path('list/', views.list_users, name='list'),
    path('roles/', views.list_roles, name='roles'),
]
