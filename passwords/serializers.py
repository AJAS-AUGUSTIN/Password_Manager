from django.conf import settings
from rest_framework import serializers
from .models import Password, SharePassword
from accounts.models import User
import urllib.request
from cryptography.fernet import Fernet

fernet = Fernet(settings.KEY)


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

    def create(self, validated_data):
        url = validated_data.get('url')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        owner = self.context['request'].user

        #encrypt data
        encrypted_email=fernet.encrypt(email.encode())
        print("EN email",encrypted_email)
        encrypted_password=fernet.encrypt(password.encode())
        print(encrypted_password)
        #decoded data
        decoded_email=encrypted_email.decode()
        print("dec em", decoded_email)
        decoded_password=encrypted_password.decode()
        print(decoded_password)

        new_password = Password(owner=owner, url=url, username=username, email=decoded_email, password=decoded_password)
        new_password.save()
        return new_password

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
        fields=['user','owner']

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Password
        fields=['url','username','email','password']