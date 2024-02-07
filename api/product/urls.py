from django.urls import path

from . import views

# Ендпоинты для Продуктов
urlpatterns = [
    path('product-simple-list/', views.ProductSimpleListView.as_view(),
         name='product-simple-list'),
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product-create/', views.CreateProductView.as_view(), name='product-create'),
    path('product-update-delete/<int:pk>/', views.ProductUpdateDeleteView.as_view(), 
         name='product-update-delete'),
    path('units-list/', views.ProductUnitsList.as_view(), name='units-list'),
    path('units-create/', views.ProductUnitsCreateView.as_view(), name='units-create'),
    path('units-update-delete/<int:pk>/', views.ProductUnitsUpdateDeleteView.as_view(), name='units-update'),
    path('product-attribute-list/', views.ProductAttributeListView.as_view(), 
         name='product-attribute-list'),
    path('product-attribute-create/', views.ProductAttributeCreateView.as_view(), 
         name='product-attribute-create'),
    path('product-attribute-update/<int:pk>/', views.ProductAttributeUpdateView.as_view(),
         name='product-attribute-update'),
    path('pp-attribute-create/', views.PPAttributeCreateView.as_view(), name='pp-attribute-create'),
    path('pp-attribute-update/<int:pk>/', views.PPAttributeUpdateView.as_view(), 
         name='pp-attribute-update'),
]