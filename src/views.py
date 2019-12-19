from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User

from .helpers import updateUser


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class UserRetrieveAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            instance = get_object_or_404(User, pk=pk)
            new_data = self.request.data
            user = updateUser(instance, new_data)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
            })
        except Exception as e:
            raise serializers.ValidationError('Invalid data for update')
