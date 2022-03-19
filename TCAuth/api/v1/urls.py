from django.urls import path
from .views import UserRegisterViewSet, UserLoginViewSet


urlpatterns = [
    path('login/', UserLoginViewSet.as_view(), name='api-login'),
    path('register/', UserRegisterViewSet.as_view(), name='api-register'),
]
