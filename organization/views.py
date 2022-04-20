from rest_framework.views import APIView
from .serializers import AddMembersSerializer, AddPasswordsSerializer, CreateOrganizationSerializer, ViewOrganizationPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import AddOrganizationPasswords, Members
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.KEY)


class CreateOrganization(APIView):
    serializer_class = CreateOrganizationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        if self.request.user.is_admin:
            return Response({'msg': "Create Organisation"})
        else:
            return Response({'msg': "Only admins can create organization"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        if self.request.user.is_admin:
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': "Only admins can create organization"}, status=status.HTTP_401_UNAUTHORIZED)


class AddMembers(APIView):
    serializer_class = AddMembersSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        if self.request.user.is_admin:
            return Response({'msg': "Add members to Organisation"})
        else:
            return Response({'msg': "Only admins can add members to organization"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        if self.request.user.is_admin:
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': "Only admins can add members to organization"}, status=status.HTTP_401_UNAUTHORIZED)



class AddPasswords(APIView):
    serializer_class = AddPasswordsSerializer
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewOrgPassword(APIView):
    serializer_class = ViewOrganizationPasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            data = AddOrganizationPasswords.objects.get(id=id)
            data.email=data.email.encode()
            data.email=fernet.decrypt(data.email)
            data.email=data.email.decode()
            data.password=data.password.encode()
            data.password=fernet.decrypt(data.password)
            data.password=data.password.decode()
            return data
        except:
            return Response({'msg':"No data"},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id, format=None):
        try:
            password = AddOrganizationPasswords.objects.get(id=id)
            org=password.organization
            user = self.request.user
            member = Members.objects.get(user=user, organization=org)
            if member:
                try:
                    serializer = self.serializer_class(self.get_object(id))
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_200_OK)
                except:
                    return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg':"Not in organization"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'msg':"Error not found"},status=status.HTTP_404_NOT_FOUND)


class ViewAllOrgPassword(APIView):
    serializer_class = ViewOrganizationPasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            user=self.request.user
            password = AddOrganizationPasswords.objects.get(id=id)
            org=password.organization
            member = Members.objects.get(user=user, organization=org)
            data = AddOrganizationPasswords.objects.filter(organization=org)
            serializer=self.serializer_class(data, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)