from rest_framework import serializers
from django.contrib.auth.models import Group
from user.models import User, Profile

# Сериалайзер для логина, обязательные две поля
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# Сериалайзер группы, разрешения
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


# Сериалайзер пользоателя, отправляется вместе 
# токенами при логине и изменении  пороля
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')


# Сериалайзер для изменеия паролей, 
# обязательные две поля, старый и новый пароль
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Сериалайзер вывода инфо профиля
class ProfileOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'