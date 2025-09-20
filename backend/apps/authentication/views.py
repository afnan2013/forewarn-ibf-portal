# Authentication views for the forewarn-ibf-portal backend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


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
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                # 'roles': [role.name for role in user.roles.all()]
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint
    """
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    username = request.data.get('username', '')

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
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # 'is_staff': user.is_staff,
                # 'roles': [role.name for role in user.roles.all()]
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
