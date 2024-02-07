from rest_framework import serializers

from stock.models import (Camera, Row, Column, Cell, CameraAttribute,
                          CameraCameraAttribute, CellAttribute, CellCellAttribute)
from product.models import Product
from api.product.serializers import (ProductDetailSerializer, )
from batch.models import Pallet, PalletPalletAttribute

class PalletAttributeFPCSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="pallet_attr_id.id")
    name = serializers.CharField(source="pallet_attr_id.title")
    class Meta:
        model = PalletPalletAttribute
        fields = ["id", "value", "attr_id", "name"]

class PalletCDSerializer(serializers.ModelSerializer):
    attributes = PalletAttributeFPCSerializer(source="pallet_attr_value", many=True)
    class Meta:
        model = Pallet
        fields = ["id", "code", "title", "description", "is_placed",
                  "is_active", "is_sent", "attributes","container_id", "product_id"]

class CellProductOutCerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CellAttrOutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="cell_attribute_id.title")
    attr_id = serializers.IntegerField(source="cell_attribute_id.id")
    class Meta:
        model = CellCellAttribute
        fields = ["id", "name", "value", "attr_id"]

class CAOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAttribute
        fields = "__all__"
        
class CCAOutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='camera_attribute_id.title')
    class Meta:
        model = CameraCameraAttribute
        fields = ("name", "value")

class ProductCellOutSerializer(serializers.ModelSerializer):
    pallet = PalletCDSerializer(source="pallet_id")
    attribute = CellAttrOutSerializer(source="cell_attribute", many=True)
    product = CellProductOutCerializer(source="product_id")
    class Meta:
        model = Cell
        fields = ["id", "code", "position", "product", "pallet", "is_full", "attribute"]

class CellListSerializer(serializers.ModelSerializer):
    product = CellProductOutCerializer(source='product_id')
    pallet = PalletCDSerializer(source="pallet_id")
    class Meta:
        model = Cell
        fields = ["id", "code", "position", "pallet", "is_full", "product"]

class ColumnListSerializer(serializers.ModelSerializer):
    cells = CellListSerializer(many=True, source="column_cell")
    class Meta:
        model = Column
        fields = ("code", "position", "cells")

class RowListSerializer(serializers.ModelSerializer):
    columns = ColumnListSerializer(many=True, source="row_column")
    class Meta:
        model = Row
        fields = ("code", "position", "columns")

class CameraListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "code", "title", "description", "position", "total_cells", 
                  "empty_cells")
        
class CameraDetailSerializer(serializers.ModelSerializer):
    rows = RowListSerializer(source='camera_row', many=True)
    attrs = CCAOutSerializer(source="camera_attribute", many=True)
    class Meta:
        model = Camera
        fields = ("id", "code", "title", "description", "position", "total_cells", 
                  "empty_cells", 'attrs', "rows")