from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView


class RegistrationView(APIView):
    pass


class ActivationView(APIView):
    pass


class LoginView(ObtainAuthToken):
    pass


class LogoutView(APIView):
    pass


class ChangePasswordView(APIView):
    pass


class ForgotPasswordView(APIView):
    pass
