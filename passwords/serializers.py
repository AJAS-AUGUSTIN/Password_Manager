from rest_framework import serializers
from .models import Password, SharePassword
from accounts.models import User
import urllib.request


class CreatePasswordSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Password
        fields = [
            'url',
            'username',
            'email',
            'password',
            'owner',
        ]

    # def create(self, validated_data):
    #     url = validated_data.get('url')
    #     username = validated_data.get('username')
    #     email = validated_data.get('email')
    #     password = validated_data.get('password')

    #     passw = Password(url=url, username=username, email=email, password=password)
    #     passw.set_password(password)
    #     passw.save()
    #     return passw

class SinglePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Password
        fields='__all__'


class PasswordViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Password
        fields='__all__'


class SharePasswordSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=SharePassword
        fields=['user','password','owner']

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Password
        fields=['url','username','email','password']