from django.urls import path

from . import views

# Ендпоинты для Склада
urlpatterns = [
    path('camera-list/', views.CameraListView.as_view(), name='stock-list'),
    path('camera-detail/<int:pk>/', views.CameraDetailView.as_view(),
         name='camera-detail'),
    path('cell-detail/<int:pk>/', views.CellDetailView.as_view(), name='cell-detail'),
]