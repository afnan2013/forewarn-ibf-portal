from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for user groups"""
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data (read-only)"""
    groups = GroupSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 
            'full_name', 'is_staff', 'is_active', 'date_joined', 
            'groups'
        ]
        read_only_fields = ['id', 'date_joined', 'is_staff', 'is_active']
    
    def get_full_name(self, obj):
        """Return full name or username as fallback"""
        return obj.get_full_name_or_username()


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (admin view)"""
    groups = GroupSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'is_staff', 'is_active', 'date_joined', 'groups'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        """Return full name or username as fallback"""
        return obj.get_full_name_or_username()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates (self-update)"""
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        user = self.instance
        if user and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def validate_username(self, value):
        """Validate username uniqueness"""
        user = self.instance
        if user and User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Username already in use.")
        return value


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin user updates"""
    groups = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Group.objects.all(), 
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'groups']
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        user = self.instance
        if user and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def validate_username(self, value):
        """Validate username uniqueness"""
        user = self.instance
        if user and User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Username already in use.")
        return value
    
    def validate(self, attrs):
        """Check if user is superuser"""
        if self.instance and self.instance.is_superuser:
            raise serializers.ValidationError("Cannot update superuser.")
        return attrs
    
    def update(self, instance, validated_data):
        """Update user with groups"""
        groups = validated_data.pop('groups', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update groups if provided
        if groups is not None:
            instance.groups.set(groups)
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password changes by admin"""
    new_password = serializers.CharField(write_only=True)
    
    def validate_new_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        """Check if target user is superuser"""
        user = self.context.get('user')
        if user and user.is_superuser:
            raise serializers.ValidationError("Cannot change password for superuser.")
        return attrs
    
    def save(self, **kwargs):
        """Set the new password"""
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserActivationSerializer(serializers.Serializer):
    """Serializer for user activation/deactivation"""
    
    def validate(self, attrs):
        """Check if user is superuser"""
        user = self.context.get('user')
        if user and user.is_superuser:
            action = self.context.get('action', 'modify')
            raise serializers.ValidationError(f"Cannot {action} superuser.")
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with groups for admin operations"""
    groups = GroupSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'is_staff', 'is_active', 'is_superuser',
            'date_joined', 'last_login', 'groups'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'is_superuser'
        ]
    
    def get_full_name(self, obj):
        """Return full name or username as fallback"""
        return obj.get_full_name_or_username()
