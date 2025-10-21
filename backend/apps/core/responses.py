"""
Standardized API Response utility for consistent response format
"""
from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """
    Standardized API response handler for consistent response format across all endpoints
    """
    
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Standard success response format
        
        Args:
            data: The response data (dict, list, or serialized data)
            message: Optional success message
            status_code: HTTP status code (default: 200)
            
        Returns:
            Response object with standardized success format
        """
        response_data = {
            'success': True,
            'message': message,
            'data': data
        }
        
        # Remove None values to keep response clean
        response_data = {k: v for k, v in response_data.items() if v is not None}
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Standard error response format
        
        Args:
            message: Error message
            errors: Detailed error information (dict or list)
            status_code: HTTP status code (default: 400)
            
        Returns:
            Response object with standardized error format
        """
        response_data = {
            'success': False,
            'message': message,
            'errors': errors
        }
        
        # Remove None values to keep response clean
        response_data = {k: v for k, v in response_data.items() if v is not None}
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(data=None, message="Resource created successfully", status_code=status.HTTP_201_CREATED):
        """
        Standard creation response format
        
        Args:
            data: The created resource data
            message: Success message
            status_code: HTTP status code (default: 201)
            
        Returns:
            Response object with standardized creation format
        """
        return APIResponse.success(data=data, message=message, status_code=status_code)
    
    @staticmethod
    def deleted(message="Resource deleted successfully", status_code=status.HTTP_200_OK):
        """
        Standard deletion response format
        
        Args:
            message: Success message
            status_code: HTTP status code (default: 200)
            
        Returns:
            Response object with standardized deletion format
        """
        return APIResponse.success(message=message, status_code=status_code)
    
    @staticmethod
    def unauthorized(message="Authentication required"):
        """
        Standard unauthorized response format
        """
        return APIResponse.error(message=message, status_code=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(message="Permission denied"):
        """
        Standard forbidden response format
        """
        return APIResponse.error(message=message, status_code=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def not_found(message="Resource not found"):
        """
        Standard not found response format
        """
        return APIResponse.error(message=message, status_code=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def validation_error(errors, message="Validation failed"):
        """
        Standard validation error response format
        
        Args:
            errors: Validation error details (typically from serializer.errors)
            message: Error message
            
        Returns:
            Response object with standardized validation error format
        """
        return APIResponse.error(message=message, errors=errors, status_code=status.HTTP_400_BAD_REQUEST)
