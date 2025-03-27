from api_parque.models import User,  TypeUser
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
class RegisterUsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id' ,'first_name', 'last_name', 'age', 'email', 'phone', 'type_id', 'password']

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            # Generar token JWT
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user
            }
        
class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeUser
        fields = ["id", "type_user"]  # Devuelve ambos valores


class TableUsersSerializer(serializers.ModelSerializer):
    type_id = TypeUserSerializer()
    age = serializers.SerializerMethodField()  # Calculamos la edad dinámicamente

    def get_age(self, obj):
        """Calcula la edad a partir de la fecha de nacimiento."""
        if obj.age:  # Asegurar que el campo no sea nulo
            today = date.today()
            return today.year - obj.age.year - ((today.month, today.day) < (obj.age.month, obj.age.day))
        return None  # En caso de que no haya fecha de nacimiento
    
    class Meta:
        model = User
        fields = ['id' ,'first_name', 'last_name', 'age', 'email', 'phone', 'type_id', 'password']

       
        
