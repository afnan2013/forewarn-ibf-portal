# Dashboard views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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
    
    return Response(stats, status=status.HTTP_200_OK)


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
            'roles': [role.name for role in request.user.roles.all()]
        },
        'permissions': [],
        'recent_actions': []
    }
    
    return Response(overview, status=status.HTTP_200_OK)
