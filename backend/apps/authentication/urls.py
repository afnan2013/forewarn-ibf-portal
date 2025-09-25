from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Permission management endpoints
    path('permissions/', views.get_frontend_permissions, name='get_frontend_permissions'),
    
    # Group management endpoints
    path('groups/', views.get_groups, name='get_groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.get_group_detail, name='get_group_detail'),
    path('groups/<int:group_id>/update/', views.update_group, name='update_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
]
