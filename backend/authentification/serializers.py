from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from users.models import StudentProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'email_verified', 'date_joined', 'force_password_change')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_input = attrs.get(self.username_field)
        password = attrs.get('password')
        
        print(f"DEBUG: Login attempt with input: {username_input}")

        if username_input and username_input.isdigit() and len(username_input) == 12:
            print("DEBUG: Detected 12-digit matricule")
            try:
                student_profile = StudentProfile.objects.get(student_number=username_input)
                attrs[self.username_field] = student_profile.user.email
                print(f"DEBUG: Found student user: {student_profile.user.email}")
            except StudentProfile.DoesNotExist:
                print("DEBUG: StudentProfile not found for this matricule")
                pass
        else:
            print("DEBUG: Treating as email or invalid format")
        
        try:
            data = super().validate(attrs)
            print("DEBUG: Authentication successful")
        except Exception as e:
            print(f"DEBUG: Authentication failed with error: {e}")
            raise e
        
        data.update({
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'email_verified': self.user.email_verified,
            'force_password_change': getattr(self.user, 'force_password_change', False)
        })
        return data

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)