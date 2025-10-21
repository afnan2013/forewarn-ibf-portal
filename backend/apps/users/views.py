from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

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

    return Response({'success': True, 'profile': profile_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['users.view_user'], raise_exception=True)
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

    return Response({'success': True, 'users': users_data, 'count': len(users_data)}, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Authenticated user can update their own profile: email, username, first_name, last_name
    """
    user = request.user
    data = request.data

    email = data.get('email')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if email and email != user.email:
        if user.__class__.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user.email = email

    if username and username != user.username:
        if user.__class__.objects.filter(username=username).exclude(pk=user.pk).exists():
            return Response({'error': 'Username already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user.username = username

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    user.save()

    return Response({
        'success': True,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@permission_required(['users.delete_user'], raise_exception=True)
def delete_user(request, user_id):
    """
    Admin endpoint to delete a user by user_id
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        return Response({'error': 'Cannot delete superuser.'}, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({'success': True, 'message': f'User {user_id} deleted.'}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required(['users.change_user'], raise_exception=True)
def activate_user(request, user_id):
    """
    Admin endpoint to activate a user (set is_active=True)
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        return Response({'error': 'Cannot activate superuser.'}, status=status.HTTP_403_FORBIDDEN)
    if user.is_active:
        return Response({'error': 'User is already active.'}, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = True
    user.save()
    return Response({'success': True, 'message': f'User {user_id} activated.'}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required(['users.change_user'], raise_exception=True)
def deactivate_user(request, user_id):
    """
    Admin endpoint to deactivate a user (set is_active=False)
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        return Response({'error': 'Cannot deactivate superuser.'}, status=status.HTTP_403_FORBIDDEN)
    if not user.is_active:
        return Response({'error': 'User is already deactivated.'}, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = False
    user.save()
    return Response({'success': True, 'message': f'User {user_id} deactivated.'}, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
@permission_required(['users.change_user'], raise_exception=True)
def update_user_by_admin(request, user_id):
    """
    Admin endpoint to update any user's profile fields (email, username, first_name, last_name, groups)
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        return Response({'error': 'Cannot update superuser.'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    email = data.get('email')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    groups = data.get('groups')

    if email and email != user.email:
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user.email = email

    if username and username != user.username:
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            return Response({'error': 'Username already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user.username = username

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    user.save()

    if groups is not None:
        from django.contrib.auth.models import Group
        try:
            group_objs = Group.objects.filter(id__in=groups)
            if len(groups) != group_objs.count():
                return Response({'error': 'One or more group IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.set(group_objs)
        except Exception as e:
            return Response({'error': f'Failed to update groups: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'success': True,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': [{'id': group.id, 'name': group.name} for group in user.groups.all()]
        }
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required(['users.change_user'], raise_exception=True)
def change_password_by_admin(request, user_id):
    """
    Admin endpoint to change any user's password
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        return Response({'error': 'Cannot change password for superuser.'}, status=status.HTTP_403_FORBIDDEN)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'success': True, 'message': f'Password changed for user {user_id}.'}, status=status.HTTP_200_OK)