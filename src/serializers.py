from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'style': {
            'input_type': 'password', 'placeholder': 'Password'}, 'write_only': True}, }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        instance = User.objects.create_user(
            email, password)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, required=True, style={
                                     'input_type': 'password', 'placeholder': 'password'})
    # setting for password field
    extra_kwargs = {'password': {'style': {
        'input_type': 'password', 'placeholder': 'Password'}, 'write_only': True}}

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect email or password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

