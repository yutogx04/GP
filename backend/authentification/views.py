from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    CustomTokenObtainPairSerializer, 
    UserSerializer, 
    PasswordChangeSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view supporting both email and matricule"""
    serializer_class = CustomTokenObtainPairSerializer


class CurrentUserView(APIView):
    """Get current authenticated user info"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        
        if hasattr(request.user, 'student_profile'):
            profile = request.user.student_profile
            data['student_profile'] = {
                'id': profile.id,
                'student_number': profile.student_number,
                'niveau_etude': profile.niveau_etude,
                'specialite': profile.specialite,
                'faculty': profile.faculty,
                'university': profile.university,
                'phone': profile.phone,
                'average_grade': profile.average_grade,
            }
        
        return Response(data)
    
    def patch(self, request):
        """Update current user profile"""
        user = request.user
        
        for field in ['first_name', 'last_name']:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        
        if hasattr(user, 'student_profile') and any(k in request.data for k in ['phone', 'niveau_etude', 'specialite', 'faculty']):
            profile = user.student_profile
            for field in ['phone', 'niveau_etude', 'specialite', 'faculty']:
                if field in request.data:
                    setattr(profile, field, request.data[field])
            profile.save()
        
        return Response(UserSerializer(user).data)


class ChangePasswordView(APIView):
    """Change password for authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ['Current password is incorrect']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.force_password_change = False
            user.save()
            
            return Response({'detail': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """Request password reset email"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'detail': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            from notifications.email_service import send_password_reset_email
            send_password_reset_email(user)
            
        except User.DoesNotExist:
            pass  # Don't reveal if email exists
        
        return Response({'detail': 'If that email exists, a reset link has been sent'})


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([uid, token, new_password]):
            return Response(
                {'detail': 'Missing required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            if not default_token_generator.check_token(user, token):
                return Response(
                    {'detail': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(new_password)
            user.force_password_change = False
            user.save()
            
            return Response({'detail': 'Password reset successfully'})
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'detail': 'Invalid reset link'},
                status=status.HTTP_400_BAD_REQUEST
            )
