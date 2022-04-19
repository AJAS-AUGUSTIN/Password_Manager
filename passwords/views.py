from urllib import request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Password, SharePassword
from passwords.serializers import CreatePasswordSerializer, PasswordViewSerializer, SinglePasswordSerializer, SharePasswordSerializer, ShareSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOwner


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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(data, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class ViewPasswordOnly(APIView):
    serializer_class = SharePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(view=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditPasswordOnly(APIView):
    serializer_class = SharePasswordSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(edit=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
                    passs= Password.objects.get(id=i.password.id)
                    serializer = self.serializer_class1(passs)
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
            if share:
                for i in share:
                    passs= Password.objects.get(id=i.password.id)
                    serializer = self.serializer_class(passs)
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg':"No Permission"},status=status.HTTP_404_NOT_FOUND)

        except:
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