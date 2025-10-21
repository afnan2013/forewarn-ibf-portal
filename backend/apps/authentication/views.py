# Authentication views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.core.responses import APIResponse

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return APIResponse.validation_error(
            errors={'username': 'Username is required', 'password': 'Password is required'},
            message='Username and password are required'
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        user_data = {
            'access_token': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'permissions': sorted(user.get_all_permissions()),
                'groups': [group.name for group in user.groups.all()]
            }
        }
        return APIResponse.success(data=user_data, message='Login successful')
    else:
        return APIResponse.unauthorized(message='Invalid credentials')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['users.add_user'], raise_exception=True)
def register_view(request):
    """
    User registration endpoint
    """
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    username = request.data.get('username', '')
    group_ids = request.data.get('group_ids', [])

    # Validation
    errors = {}
    if not email:
        errors['email'] = 'Email is required'
    if not password:
        errors['password'] = 'Password is required'
    if not username:
        errors['username'] = 'Username is required'
        
    if errors:
        return APIResponse.validation_error(errors=errors)
    
    if User.objects.filter(email=email).exists():
        return APIResponse.error(message='User with this email already exists')

    if User.objects.filter(username=username).exists():
        return APIResponse.error(message='User with this username already exists')
    
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            

            if group_ids:
                groups = Group.objects.filter(id__in=group_ids)
                user.groups.set(groups)
                
            user_data = {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'groups': [{'id': group.id, 'name': group.name} for group in user.groups.all()]
            }
            return APIResponse.created(data=user_data, message='User created successfully')
    
    except Exception as e:
        return APIResponse.error(message='Failed to create user', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout_view(request):
    """
    User logout endpoint (for token blacklisting in future)
    """
    return APIResponse.success(message='Successfully logged out')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.add_group'], raise_exception=True)
def get_frontend_permissions(request):
    # Define which content types to show in frontend
    allowed_content_types = ['user', 'group']
    
    # Filter permissions for only user and group models
    permissions = Permission.objects.filter(
        content_type__model__in=allowed_content_types
    ).select_related('content_type').order_by('content_type__model', 'codename')
    
    permission_data = []
    for perm in permissions:
        permission_data.append({
            'id': perm.id,
            'name': perm.name,
            'codename': perm.codename,
            'content_type': perm.content_type.name,
        })
    
    return APIResponse.success(
        data={'permissions': permission_data, 'count': len(permission_data)},
        message='Frontend permissions retrieved successfully'
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.add_group'], raise_exception=True)
def create_group(request):
    """
    Create a new group with permissions
    Expected payload: {'name': 'group_name', 'permission_ids': [1, 2, 3]}
    """
    
    group_name = request.data.get('name')
    permission_ids = request.data.get('permission_ids', [])
    
    # Validate input
    if not group_name:
        return APIResponse.validation_error(
            errors={'name': 'Group name is required'},
            message='Group name is required'
        )
    
    # Check if group already exists
    if Group.objects.filter(name=group_name).exists():
        return APIResponse.error(message='Group with this name already exists')
    
    try:
        with transaction.atomic():
            # Create the group
            group = Group.objects.create(name=group_name)
            
            # Add permissions to the group
            if permission_ids:
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)
            
            group_data = {
                'id': group.id,
                'name': group.name,
                'permissions': [
                    {
                        'id': perm.id,
                        'name': perm.name,
                        'codename': perm.codename
                    }
                    for perm in group.permissions.all()
                ]
            }
            return APIResponse.created(data=group_data, message='Group created successfully')
            
    except Exception as e:
        return APIResponse.error(
            message='Failed to create group', 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.change_group'], raise_exception=True)
def update_group(request, group_id):
    """
    Update group and attach/detach permissions
    Expected payload: {'name': 'new_name', 'permission_ids': [1, 2, 3]}
    """
    try:
        group = get_object_or_404(Group, id=group_id)
        
        group_name = request.data.get('name')
        permission_ids = request.data.get('permission_ids')
        
        with transaction.atomic():
            # Update group name if provided
            if group_name and group_name != group.name:
                # Check if new name already exists
                if Group.objects.filter(name=group_name).exclude(id=group_id).exists():
                    return APIResponse.error(message='Group with this name already exists')
                group.name = group_name
                group.save()
            
            # Update permissions if provided
            if permission_ids is not None:
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)
            
            group_data = {
                'id': group.id,
                'name': group.name,
                'permissions': [
                    {
                        'id': perm.id,
                        'name': perm.name,
                        'codename': perm.codename
                    }
                    for perm in group.permissions.all()
                ]
            }
            return APIResponse.success(data=group_data, message='Group updated successfully')
            
    except Exception as e:
        return APIResponse.error(
            message='Failed to update group', 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.delete_group'], raise_exception=True)
def delete_group(request, group_id):
    """
    Delete a group
    """
    try:
        group = get_object_or_404(Group, id=group_id)
        
        # Store group info before deletion
        group_info = {
            'id': group.id,
            'name': group.name,
            'permission_count': group.permissions.count(),
            'user_count': group.user_set.count()
        }
        
        group.delete()
        
        return APIResponse.success(
            data=group_info, 
            message=f'Group "{group_info["name"]}" deleted successfully'
        )
        
    except Exception as e:
        return APIResponse.error(
            message='Failed to delete group', 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.view_group'], raise_exception=True)
def get_groups(request):
    """
    Get all groups with their permissions
    """
    groups = Group.objects.all().prefetch_related('permissions')
    
    groups_data = []
    for group in groups:
        groups_data.append({
            'id': group.id,
            'name': group.name,
            'user_count': group.user_set.count(),
            'permissions': [
                {
                    'id': perm.id,
                    'name': perm.name,
                    'codename': perm.codename,
                    'content_type': perm.content_type.model
                }
                for perm in group.permissions.all()
            ]
        })
    
    return APIResponse.success(
        data={'groups': groups_data, 'count': len(groups_data)},
        message='Groups retrieved successfully'
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.view_group'], raise_exception=True)
def get_group_detail(request, group_id):
    """
    Get detailed information about a specific group
    """
    try:
        group = get_object_or_404(Group, id=group_id)
        
        group_data = {
            'id': group.id,
            'name': group.name,
            'user_count': group.user_set.count(),
            'users': [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
                for user in group.user_set.all()
            ],
            'permissions': [
                {
                    'id': perm.id,
                    'name': perm.name,
                    'codename': perm.codename,
                    'content_type': {
                        'id': perm.content_type.id,
                        'app_label': perm.content_type.app_label,
                        'model': perm.content_type.model,
                        'name': perm.content_type.name
                    }
                }
                for perm in group.permissions.all()
            ]
        }
        return APIResponse.success(data=group_data, message='Group details retrieved successfully')
        
    except Exception as e:
        return APIResponse.error(
            message='Failed to get group details', 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Authenticated user can change their own password
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return APIResponse.validation_error(
            errors={'old_password': 'Required', 'new_password': 'Required'},
            message='Old and new password are required'
        )

    if not user.check_password(old_password):
        return APIResponse.validation_error(
            errors={'old_password': 'Incorrect password'},
            message='Old password is incorrect'
        )

    user.set_password(new_password)
    user.save()

    return APIResponse.success(message='Password changed successfully')
