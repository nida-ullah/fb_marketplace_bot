from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FacebookAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'confirm_password', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class FacebookAccountSerializer(serializers.ModelSerializer):
    session_exists = serializers.SerializerMethodField()

    class Meta:
        model = FacebookAccount
        fields = ['id', 'email', 'password', 'session_exists', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_session_exists(self, obj):
        import os
        session_file = f"sessions/{obj.email.replace('@', '_').replace('.', '_')}.json"
        return os.path.exists(session_file)
