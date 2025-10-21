from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_password_changed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
    
    def soft_delete(self):
        """Soft delete user"""
        self.is_deleted = True
        self.is_active = False
        self.save()
    
    def get_full_name_or_username(self):
        """Return full name or username as fallback"""
        return self.get_full_name() or self.username