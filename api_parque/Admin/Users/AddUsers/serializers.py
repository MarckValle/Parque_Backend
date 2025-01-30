from api_parque.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email', 'phone', 'type_id', 'password']

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            # Generar token JWT
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user
            }
