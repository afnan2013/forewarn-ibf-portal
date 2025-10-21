from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from apps.core.responses import APIResponse
from .serializers import (
    UserProfileSerializer, 
    UserListSerializer, 
    UserUpdateSerializer,
    AdminUserUpdateSerializer,
    ChangePasswordSerializer,
    UserActivationSerializer,
    UserDetailSerializer
)
from .permissions import (
    HasUserViewPermission,
    HasUserChangePermission, 
    HasUserDeletePermission,
    CannotModifySuperuser,
)

User = get_user_model()


class UserProfileView(generics.RetrieveAPIView):
    """
    Get current user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(
            data=serializer.data, 
            message='User profile retrieved successfully'
        )


class UserListView(generics.ListAPIView):
    """
    List all users (admin only)
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, HasUserViewPermission]
    
    def get_queryset(self):
        return User.objects.filter(is_deleted=False).select_related().prefetch_related('groups')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data={
                'users': serializer.data,
                'count': queryset.count()
            },
            message='Users retrieved successfully'
        )


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Authenticated user can update their own profile: email, username, first_name, last_name
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return APIResponse.success(
                data=serializer.data,
                message='User profile updated successfully'
            )
        else:
            return APIResponse.validation_error(
                message='Validation failed',
                errors=serializer.errors
            )


class UserDeleteView(generics.DestroyAPIView):
    """
    Admin endpoint to delete a user by user_id
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, HasUserDeletePermission, CannotModifySuperuser]
    lookup_url_kwarg = 'user_id'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            return APIResponse.forbidden(message='Cannot delete superuser')
        
        user_id = instance.id
        instance.delete()
        return APIResponse.success(message=f'User {user_id} deleted successfully')


class UserActivateView(APIView):
    """
    Admin endpoint to activate a user (set is_active=True)
    """
    permission_classes = [IsAuthenticated, HasUserChangePermission]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        
        # Validate with serializer
        serializer = UserActivationSerializer(
            data={}, 
            context={'user': user, 'action': 'activate'}
        )
        
        if not serializer.is_valid():
            return APIResponse.validation_error(
                message='Validation failed',
                errors=serializer.errors
            )
        
        if user.is_active:
            return APIResponse.error(message='User is already active')
        
        user.is_active = True
        user.save()
        return APIResponse.success(message=f'User {user_id} activated successfully')


class UserDeactivateView(APIView):
    """
    Admin endpoint to deactivate a user (set is_active=False)
    """
    permission_classes = [IsAuthenticated, HasUserChangePermission]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        
        # Validate with serializer
        serializer = UserActivationSerializer(
            data={}, 
            context={'user': user, 'action': 'deactivate'}
        )
        
        if not serializer.is_valid():
            return APIResponse.validation_error(
                message='Validation failed',
                errors=serializer.errors
            )
        
        if not user.is_active:
            return APIResponse.error(message='User is already deactivated')
        
        user.is_active = False
        user.save()
        return APIResponse.success(message=f'User {user_id} deactivated successfully')


class AdminUserUpdateView(generics.UpdateAPIView):
    """
    Admin endpoint to update any user's profile fields (email, username, first_name, last_name, groups)
    """
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAuthenticated, HasUserChangePermission, CannotModifySuperuser]
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_user = serializer.save()
            # Use UserDetailSerializer for response
            response_serializer = UserDetailSerializer(updated_user)
            return APIResponse.success(
                data={'user': response_serializer.data},
                message='User updated successfully'
            )
        else:
            return APIResponse.validation_error(
                message='Validation failed',
                errors=serializer.errors
            )


class ChangePasswordByAdminView(APIView):
    """
    Admin endpoint to change any user's password
    """
    permission_classes = [IsAuthenticated, HasUserChangePermission]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'user': user}
        )
        
        if serializer.is_valid():
            serializer.save()
            return APIResponse.success(message=f'Password changed for user {user_id}')
        else:
            return APIResponse.validation_error(
                message='Validation failed',
                errors=serializer.errors
            )


class UserDetailView(generics.RetrieveAPIView):
    """
    Get detailed user information (admin only)
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, HasUserViewPermission]
    queryset = User.objects.all().prefetch_related('groups')
    lookup_url_kwarg = 'user_id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(
            data=serializer.data,
            message='User details retrieved successfully'
        )
