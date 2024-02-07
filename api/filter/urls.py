from django.urls import path

from . import views

# Ендпоинты для Склада
urlpatterns = [
    path('cell-log/', views.CellLogList.as_view(), name='cell-log'),
    path('batch-filter/', views.BatchFilterView.as_view(), 
         name='batch-filter'),
    path('transfer-filter/', views.TransferFilterView.as_view(), 
         name="transfer-filter"),
    path('product-filter/', views.ProductFilterView.as_view(),
         name="product-filter"),
    path('cell-create/', views.CreateCellsView.as_view(),
         name="cell-create"),
    path('camera-cells-create/', views.CreateCameraCells.as_view(),
         name="camera-cells-create"),
    path('logs-delete/', views.DeleteColumnCells.as_view(), name='logs-delete'),
]