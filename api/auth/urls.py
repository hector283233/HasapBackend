from django.urls import path

from . import views

# Ендпоинты для авторизации
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('current-profile/', views.CurrentProfile.as_view(), name='current-profile'),
    path('profile-list/', views.ProfileList.as_view(), name='profiles'),
]