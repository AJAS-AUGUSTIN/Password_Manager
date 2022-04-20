from pyexpat import model
from rest_framework import serializers
from .models import Members, Organization, AddOrganizationPasswords
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.KEY)


class CreateOrganizationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Organization
        fields = '__all__'


class AddMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class AddPasswordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOrganizationPasswords
        fields = '__all__'

    def create(self, validated_data):
        url = validated_data.get('url')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        organization = validated_data.get('organization')

        owner = self.context['request'].user
        if organization.owner==owner:
            #encrypt data
            encrypted_email=fernet.encrypt(email.encode())
            encrypted_password=fernet.encrypt(password.encode())
            #decoded data
            decoded_email=encrypted_email.decode()
            decoded_password=encrypted_password.decode()

            new_password = AddOrganizationPasswords(organization=organization, url=url, username=username, email=decoded_email, password=decoded_password)
            new_password.save()
            return new_password
        else:
            raise serializers.ValidationError("No permission. Only owners can add password!")


class ViewOrganizationPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOrganizationPasswords
        fields = '__all__'

