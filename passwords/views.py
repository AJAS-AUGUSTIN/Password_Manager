from urllib import request
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Password, SharePassword
from passwords.serializers import CreatePasswordSerializer, PasswordViewSerializer, SinglePasswordSerializer, SharePasswordSerializer, ShareSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOwner
from cryptography.fernet import Fernet

fernet = Fernet(settings.KEY)


class CreatePassword(APIView):
    serializer_class = CreatePasswordSerializer
    
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

class SinglePassword(APIView):
    serializer_class=SinglePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, id):
        try:
            data = Password.objects.get(id=id)
            self.check_object_permissions(self.request, data)
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
            serializer = self.serializer_class(self.get_object(id))
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:
            return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        data = self.get_object(id)
        serializer = self.serializer_class(
            data, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        data = self.get_object(id)
        data.delete()
        return Response(status=status.HTTP_200_OK)


class PasswordView(APIView):
    serializer_class = PasswordViewSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, format=None):
        try:
            user=self.request.user
            data = Password.objects.filter(owner=user)
            serializer=self.serializer_class(data, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ViewPasswordOnly(APIView):
    serializer_class = SharePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id , format=None):
        password = Password.objects.get(id=id)
        owner = self.request.user
        if owner == password.owner:
            return Response({'msg':'share password'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':"NO permission"})


    def post(self, request, id, format=None):
        password = Password.objects.get(id=id)
        owner = self.request.user
        if owner == password.owner:
            serializer = self.serializer_class(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(view=True, password=password)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':"NO permission"})




class EditPasswordOnly(APIView):
    serializer_class = SharePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id , format=None):
        password = Password.objects.get(id=id)
        owner = self.request.user
        if owner == password.owner:
            return Response({'msg':'share password'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':"NO permission"})

    def post(self, request, id, format=None):
        password = Password.objects.get(id=id)
        owner = self.request.user
        if owner == password.owner:
            serializer = self.serializer_class(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(edit=True, password=password)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':"NO permission"})



class SharedViewSinglePassword(APIView):
    serializer_class=SharePasswordSerializer
    serializer_class1=SinglePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            data = Password.objects.get(id=id)
            datas= data.id
            user=self.request.user.id
            share = SharePassword.objects.filter(user=user, view=True, password=datas)
            if share:
                for i in share:
                    data= Password.objects.get(id=i.password.id)
                    data.email=data.email.encode()
                    data.email=fernet.decrypt(data.email)
                    data.email=data.email.decode()
                    data.password=data.password.encode()
                    data.password=fernet.decrypt(data.password)
                    data.password=data.password.decode()
                    # data.save()
                    serializer = self.serializer_class1(data)
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)


class SharedEditSinglePassword(APIView):
    serializer_class=ShareSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            data = Password.objects.get(id=id)
            datas= data.id
            user=self.request.user.id
            share = SharePassword.objects.filter(user=user, edit=True, password=datas)
            print("Shareeeeeeeee",share)
            if share:
                for i in share:
                    data= Password.objects.get(id=i.password.id)
                    data.email=data.email.encode()
                    data.email=fernet.decrypt(data.email)
                    data.email=data.email.decode()
                    data.password=data.password.encode()
                    data.password=fernet.decrypt(data.password)
                    data.password=data.password.decode()
                    serializer = self.serializer_class(data)
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

        except:
            print("Exceptttt")
            return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        try:
            data = Password.objects.get(id=id)
            datas= data.id
            user=self.request.user.id
            share = SharePassword.objects.filter(user=user, edit=True, password=datas)
            if share:
                for i in share:
                    passs= Password.objects.get(id=i.password.id)
                    serializer = self.serializer_class(passs, data=request.data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        serialized_data = serializer.data
                        return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)