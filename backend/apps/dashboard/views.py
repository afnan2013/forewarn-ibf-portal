# Dashboard views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.core.responses import APIResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics
    """
    # Placeholder for dashboard statistics
    stats = {
        'total_users': 0,
        'active_alerts': 0,
        'recent_activities': [],
        'system_status': 'operational'
    }
    
    return APIResponse.success(
        data=stats, 
        message='Dashboard statistics retrieved successfully'
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """
    Get dashboard overview data
    """
    # Placeholder for dashboard overview
    overview = {
        'user': {
            'id': str(request.user.id),
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'groups': [group.name for group in request.user.groups.all()]
        },
        'permissions': list(request.user.get_all_permissions()),
        'recent_actions': []
    }
    
    return APIResponse.success(
        data=overview, 
        message='Dashboard overview retrieved successfully'
    )
