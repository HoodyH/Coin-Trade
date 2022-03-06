from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):

    confirm_password = CharField(style={'input_type': 'password'}, write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
            }
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
