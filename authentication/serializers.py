from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"inut_type": "password"})
    extra_kwargs = {"password": {"write_only": True}}

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "status",
        ]

    def save(self):
        reg = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            password=make_password(self.validated_data["password"]),
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            mobile_phone=self.validated_data["mobile_phone"],
        )
        reg.save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "date_joined",
            "status",
        ]


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={"input_type": "password"})


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirmpassword = serializers.CharField(max_length=128)
