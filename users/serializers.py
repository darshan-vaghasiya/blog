from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'validators': [UniqueValidator(CustomUser.objects.all(), lookup='iexact',
                                                     message='user with this email address already exists.')],
                      'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True, 'error_messages': {'invalid_choice': "Role should be author or reader."}},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assignment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user
