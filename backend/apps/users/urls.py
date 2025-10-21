from django.urls import path
from . import views

# User management URLs
# These handle user CRUD operations

app_name = 'users'

urlpatterns = [
    # User endpoints
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.update_user_profile, name='update_profile'),
    
    # # Admin Endpoints
    path('list/', views.list_users, name='list'),
    path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('<int:user_id>/activate/', views.activate_user, name='activate_user'),
    path('<int:user_id>/update/', views.update_user_by_admin, name='update_user_by_admin'),
    path('<int:user_id>/change-password/', views.change_password_by_admin, name='change_password_by_admin'),
]
