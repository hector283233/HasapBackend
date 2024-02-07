from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User, Profile
from django.db import models
from widgets import PastCustomDatePickerWidget
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as AuthGroupAdmin

class CustomUserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        
# Админка пользователя, удалил некоторые не нужные 
# из видимых облостей
class UserAdmin(AuthUserAdmin):
    # Показывает полей изменения данных пользователя
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    # Показывает полей регистрации пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("username", "is_staff")
    
    form = CustomUserChange

# Админка Профиля
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Изменил календарь чтобы легко найти год рождения
    formfield_overrides = {
        models.DateField: {'widget':PastCustomDatePickerWidget}
    }

admin.site.register(User, UserAdmin)