from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Role(models.Model):
    """
    Dynamic role management system
    Roles can be created, modified, and deleted through admin interface
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Role name (e.g., 'manager', 'admin', 'analyst')"
    )
    
    display_name = models.CharField(
        max_length=100,
        help_text="Human-readable role name"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of what this role can do"
    )
    
    level = models.IntegerField(
        default=1,
        help_text="Role hierarchy level (1=lowest, higher = more permissions)"
    )
    
    permissions = models.JSONField(
        default=dict,
        help_text="JSON object defining specific permissions for this role"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this role is currently active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ['level', 'name']
    
    def __str__(self):
        return f"{self.display_name} (Level {self.level})"


class User(AbstractUser):
    """
    Custom User model for FOREWARN IBF Portal
    Extends Django's built-in User with additional fields
    """
    
    # Use UUID as primary key instead of integer ID
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user"
    )
    
    # Dynamic role-based access control
    # Link to Role model for flexible role management
    user_role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="User's role (references Role model)"
    )
    
    # Fallback role string for compatibility
    role = models.CharField(
        max_length=50,
        default='user',
        help_text="Fallback role name if user_role is not set"
    )
    
    # Additional profile fields
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number"
    )
    
    organization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="User's organization or company"
    )
    
    # Timestamps (AbstractUser already has date_joined, we add updated_at)
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time user profile was updated"
    )
    
    # Email should be unique
    email = models.EmailField(
        unique=True,
        help_text="User's email address (used for login)"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        """String representation of the user"""
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_role_name(self):
        """Get the user's role name (from Role model or fallback string)"""
        if self.user_role:
            return self.user_role.name
        return self.role
    
    def get_role_level(self):
        """Get the user's role level"""
        if self.user_role:
            return self.user_role.level
        return 1  # Default level for fallback roles
    
    def get_role_permissions(self):
        """Get the user's role permissions"""
        if self.user_role:
            return self.user_role.permissions
        return {}  # No special permissions for fallback roles
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.get_role_name().lower() == role_name.lower()
    
    def has_minimum_role_level(self, min_level):
        """Check if user has at least the specified role level"""
        return self.get_role_level() >= min_level
    
    def has_permission(self, permission_key):
        """Check if user has a specific permission"""
        permissions = self.get_role_permissions()
        return permissions.get(permission_key, False)
    
    def is_admin_level(self):
        """Check if user has admin-level permissions (level 3 or higher)"""
        return self.get_role_level() >= 3
    
    def is_manager_level(self):
        """Check if user has manager-level permissions (level 2 or higher)"""
        return self.get_role_level() >= 2
