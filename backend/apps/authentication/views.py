# Authentication views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import get_object_or_404
from django.db import transaction


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            # 'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'permissions': sorted(user.get_all_permissions()),
                'group': [group.name for group in user.groups.all()]
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.add_user'], raise_exception=True)
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

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'User with this email already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
                
            return Response({
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'groups': [{'id': group.id, 'name': group.name} for group in user.groups.all()]
                }
            }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(e)
        return Response(
            {'error': 'Failed to create user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def logout_view(request):
    """
    User logout endpoint (for token blacklisting in future)
    """
    return Response(
        {'message': 'Successfully logged out'}, 
        status=status.HTTP_200_OK
    )



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
    
    return Response({
        'success': True,
        'permissions': permission_data,
        'count': len(permission_data)
    })


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
        return Response(
            {'error': 'Group name is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if group already exists
    if Group.objects.filter(name=group_name).exists():
        return Response(
            {'error': 'Group with this name already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        with transaction.atomic():
            # Create the group
            group = Group.objects.create(name=group_name)
            
            # Add permissions to the group
            if permission_ids:
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)
            
            return Response({
                'success': True,
                'message': 'Group created successfully',
                'group': {
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
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': f'Failed to create group: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.update_group'], raise_exception=True)
def update_group(request, group_id):
    """
    Update group and attach/detach permissions
    Expected payload: {'name': 'new_name', 'permission_ids': [1, 2, 3]}
    """
    # Check if user has permission to change groups
    if not request.user.has_perm('auth.change_group'):
        return Response(
            {'error': 'You do not have permission to update groups'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        group = get_object_or_404(Group, id=group_id)
        
        group_name = request.data.get('name')
        permission_ids = request.data.get('permission_ids')
        
        with transaction.atomic():
            # Update group name if provided
            if group_name and group_name != group.name:
                # Check if new name already exists
                if Group.objects.filter(name=group_name).exclude(id=group_id).exists():
                    return Response(
                        {'error': 'Group with this name already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                group.name = group_name
                group.save()
            
            # Update permissions if provided
            if permission_ids is not None:
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)
            
            return Response({
                'success': True,
                'message': 'Group updated successfully',
                'group': {
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
            })
            
    except Exception as e:
        return Response(
            {'error': f'Failed to update group: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['auth.delete_group'], raise_exception=True)
def delete_group(request, group_id):
    """
    Delete a group
    """
    # Check if user has permission to delete groups
    if not request.user.has_perm('auth.delete_group'):
        return Response(
            {'error': 'You do not have permission to delete groups'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
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
        
        return Response({
            'success': True,
            'message': f'Group "{group_info["name"]}" deleted successfully',
            'deleted_group': group_info
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to delete group: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_groups(request):
    """
    Get all groups with their permissions
    """
    # Check if user has permission to view groups
    if not request.user.has_perm('auth.view_group'):
        return Response(
            {'error': 'You do not have permission to view groups'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
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
    
    return Response({
        'success': True,
        'groups': groups_data,
        'count': len(groups_data)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_detail(request, group_id):
    """
    Get detailed information about a specific group
    """
    # Check if user has permission to view groups
    if not request.user.has_perm('auth.view_group'):
        return Response(
            {'error': 'You do not have permission to view groups'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        group = get_object_or_404(Group, id=group_id)
        
        return Response({
            'success': True,
            'group': {
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
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to get group details: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
