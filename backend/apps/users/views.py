# Users views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    profile_data = {
        'id': str(user.id),
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'groups': [{'id': group.id, 'name': group.name} 
                for group in user.groups.all()]
    }
    
    return Response(profile_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    """
    List all users (admin only)
    """
    users = User.objects.all().select_related()
    users_data = []
    
    for user in users:
        users_data.append({
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'groups': [{'id': group.id, 'name': group.name} 
                for group in user.groups.all()]
        })
    
    return Response(users_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_roles(request):
    """
    List all available roles (admin only)
    """
    roles = Role.objects.all()
    roles_data = []
    
    for role in roles:
        roles_data.append({
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'permissions': role.permissions,
            'is_active': role.is_active,
            'created_at': role.created_at
        })
    
    return Response(roles_data, status=status.HTTP_200_OK)
