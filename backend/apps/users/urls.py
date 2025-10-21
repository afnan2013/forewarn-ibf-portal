from django.urls import path
from . import views

# User management URLs
# These handle user CRUD operations using Class-Based Views

app_name = 'users'

urlpatterns = [
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    
    # Admin user management endpoints
    path('list/', views.UserListView.as_view(), name='list'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:user_id>/delete/', views.UserDeleteView.as_view(), name='delete_user'),
    path('<int:user_id>/deactivate/', views.UserDeactivateView.as_view(), name='deactivate_user'),
    path('<int:user_id>/activate/', views.UserActivateView.as_view(), name='activate_user'),
    path('<int:user_id>/update/', views.AdminUserUpdateView.as_view(), name='update_user_by_admin'),
    path('<int:user_id>/change-password/', views.ChangePasswordByAdminView.as_view(), name='change_password_by_admin'),
]
