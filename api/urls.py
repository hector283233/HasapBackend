from django.urls import path, include

urlpatterns = [
    # Ендпоинт для авторизации и пользователей
    path('auth/', include('api.auth.urls')),
    path('stock/', include('api.stock.urls')),
    path('product/', include('api.product.urls')),
    path('batch/', include('api.batch.urls')),
    path('transfer/', include('api.transfer.urls')),
    path('filter/', include('api.filter.urls')),
]