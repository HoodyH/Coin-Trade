from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserRegistrationSerializer

User = get_user_model()


class UserRegisterViewSet(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginViewSet(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })
