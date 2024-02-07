from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from api.utils import has_permission
from user.models import *
from .serializers import *

from GlobalVariables import *

# Класс для авторизации пользователей
class LoginUser(APIView):
    # Документация для фронта
    @swagger_auto_schema(
        request_body=LoginSerializer, 
        operation_summary = "Login user",
        
        # Пример ответа
        responses={200: openapi.Response(
            description="Response Example",
            examples={
            "application/json": {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjA1MTAxOSwiaWF0IjoxNjgzNDU5MDE5LCJqdGkiOiJhNjE5YjY1Nzc1MzM0M2ViODkyODQwYTFlMWZkYTdjNCIsInVzZXJfaWQiOjJ9.HnKAbLINdy-EDSt5gChD_x3VFqPb3dX6S-vZ8R9f-tU",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0OTk1MDE5LCJpYXQiOjE2ODM0NTkwMTksImp0aSI6ImE2M2MwYTRhNjJlMzQ2NjFhMTg0M2JlNTM4MjRjYWE0IiwidXNlcl9pZCI6Mn0.id9RPwPm1j9cZYfxNcz4dTvNFiJRTNXRLfgSPPcH-e8",
                "user": {"username": "Manager01", "groups": [{"name": "Stock"}, {"name": "Manager"}]}
            }})})
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            # Проверяет отправленные данные
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                
                user = authenticate(username=username, password=password) # Авторизуется
                
                # Проверяет еслтли такой прльзователь
                if user is None:
                    return Response({
                        "response": "error",
                        "err": ERR_USER_NOT_FOUND,
                        "message": MSG_USER_NOT_FOUND,
                        "data": {}
                    }, status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                
                # Возвращает токен и данные групп
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data,
                })
            else:
                return Response({"response":"error", "message": "Please enter username and password"}, 
                                status=status.HTTP_400_BAD_REQUEST)    
        except:
            return Response({"response":"error", "message": "Please enter username and password"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    # Документация для фронта
    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_summary = "Change password",
        # Пример ответа
        responses={200: openapi.Response(
            description="Response Example",
            examples={
            "application/json": {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjA1MTAxOSwiaWF0IjoxNjgzNDU5MDE5LCJqdGkiOiJhNjE5YjY1Nzc1MzM0M2ViODkyODQwYTFlMWZkYTdjNCIsInVzZXJfaWQiOjJ9.HnKAbLINdy-EDSt5gChD_x3VFqPb3dX6S-vZ8R9f-tU",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0OTk1MDE5LCJpYXQiOjE2ODM0NTkwMTksImp0aSI6ImE2M2MwYTRhNjJlMzQ2NjFhMTg0M2JlNTM4MjRjYWE0IiwidXNlcl9pZCI6Mn0.id9RPwPm1j9cZYfxNcz4dTvNFiJRTNXRLfgSPPcH-e8",
                "user": {"username": "Manager01", "groups": [{"name": "Stock"}, {"name": "Manager"}]}
            }})}
    )
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        
        # Проверяет отправленные данные
        if serializer.is_valid():
            user = request.user
            
            # Проверяет правильность прежнего пароля
            pass_check = user.check_password(data['old_password'])
            if pass_check:
                user.password = make_password(data['new_password'])
                user.save() # Сохраняет новый пароль
                username = user.username
                password = data['new_password']
                user = authenticate(username=username, password=password) # Авторизуется новым паролем
                if user is None:
                    return Response({
                        "response": "error",
                        "data": {}
                    }, status=status.HTTP_404_NOT_FOUND)
                user_serializer = UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_serializer.data,
                })
            else:
                return Response({'response':'error', 
                                 'message': 'wrong password, please enter your previous password'},
                                 status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'response':'error'})


# Профиль авторизовонного пользователя
class CurrentProfile(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: ProfileOutSerializer},
        operation_summary = "Get profile of user",
        operation_description="Need to be authorized to make this request.",
    )
    def get(self, request):
        user = request.user
        profile_exists = Profile.objects.filter(user=user).exists()
        if profile_exists:
            profile = Profile.objects.get(user=user)
            serializer = ProfileOutSerializer(profile)
            return Response({"response":"success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "message": "Profile could not be found"}, status=status.HTTP_404_NOT_FOUND)

# Профили всех пользователей, дооступен только для руководителей
class ProfileList(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: ProfileOutSerializer},
        operation_summary = "List the profiles, need to be Manager",
        operation_description="***IMPORTANT***: only users with 'Manager' permission has access.\nNeed to be authorized to make this request.",
    )
    def get(self, request):
        user = request.user
        
        # Проверяет естли у пользователя права руководителя
        if has_permission(user, MANAGER):
            profiles = Profile.objects.all()
            serializer = ProfileOutSerializer(profiles, many=True)
            return Response({"response":"success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "message": "You do not have permission for this"}, status=status.HTTP_404_NOT_FOUND)