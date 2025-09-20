from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

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
