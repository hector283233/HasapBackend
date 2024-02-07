from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Настройки документаций API для фронта
schema_view = get_schema_view(
   openapi.Info(
      title="SapHasap API",
      default_version='v1',
      description="An api for managing stock.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gylyjov.rd@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Корневые эндпоинты
urlpatterns = [
   # Корневой ендпоин API
    path("api/", include("api.urls")),
    
   #  Корневой ендпоинт админки
    path('admin/', admin.site.urls),
    
   #  Эндпоинты для API документации
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
