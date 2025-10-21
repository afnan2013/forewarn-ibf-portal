from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .models import User

# Register ContentType for admin dashboard
@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    """Admin interface for Content Types"""
    list_display = ('id', 'app_label', 'model', 'name')
    list_filter = ('app_label',)
    search_fields = ('app_label', 'model', 'name')
    ordering = ('app_label', 'model')
    readonly_fields = ('app_label', 'model')
    
    def has_add_permission(self, request):
        return False  # Don't allow adding new content types
    
    def has_delete_permission(self, request, obj=None):
        return False  # Don't allow deleting content types

# Register Permission for admin dashboard  
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin interface for Permissions"""
    list_display = ('id', 'name', 'content_type', 'codename')
    list_filter = ('content_type__app_label', 'content_type')
    search_fields = ('name', 'codename', 'content_type__model')
    ordering = ('content_type__app_label', 'content_type__model', 'codename')
    readonly_fields = ('content_type', 'codename', 'name')
    
    def has_add_permission(self, request):
        return False  # Don't allow adding new permissions manually
    
    def has_delete_permission(self, request, obj=None):
        return False  # Don't allow deleting permissions


# Register custom User model for admin dashboard
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model"""
    
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_password_changed', 'is_deleted', 'date_joined')
    
    # Fields to filter by
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_password_changed', 'is_deleted', 'date_joined', 'groups')
    
    # Fields to search
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Ordering
    ordering = ('username',)
    
    # Add your custom fields to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_password_changed', 'is_deleted'),
        }),
    )
    
    # Add custom fields to the add form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('is_password_changed', 'is_deleted'),
        }),
    )

