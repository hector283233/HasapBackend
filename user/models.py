from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup
from datetime import date
from django import forms



# Модель Пользователя, можно добавить новые атрибюты
class User(AbstractUser):
    pass

# Модель профиля
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Поьзователь')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Електронаая Почта')
    mobile = models.CharField(max_length=64, blank=True, null=True, verbose_name='Мобильный')
    phone = models.CharField(max_length=64, blank=True, null=True, verbose_name='Домашний Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    image = models.ImageField(("Фото"), upload_to = "profiles/", default="profiles/default.jpg")
    dob = models.DateField(blank=True, null=True, verbose_name='Дата Рождения')
    started_working = models.DateTimeField(blank=True, null=True, verbose_name='Дата принятия на работу')
    extra_info = models.TextField(blank=True, null=True, verbose_name='Доопольнительное Инфо')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    