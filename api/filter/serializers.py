from rest_framework import serializers

from batch.models import *
from product.models import *
from transfer.models import *
from stock.models import *
from user.models import *

class CellLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    class Meta:
        model = CellLog
        fields = ['id', 'is_full', 'created_at', 'cell_id', 'pallet_id', 'product_id']

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"

class BatchContainerSerializer(serializers.ModelSerializer):
    info = ContainerSerializer(source="container_id")
    class Meta:
        model = BatchContainer
        fields = ["id", "info"]

class BatchAttrFilterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="batch_batch_id")
    class Meta:
        model = BatchBatchAttribute
        fields = ["id", "name", "value", "batch_batch_id"]

class BatchFilterSerializer(serializers.ModelSerializer):
    attributes = BatchAttrFilterSerializer(source="batch_value", many=True)
    class Meta:
        model = Batch
        fields = ["id", "title", "description", "arrived_at", "attributes"]

class UserFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PCTransferListAttributeFiltersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="pctransfer_attribute_id.title")
    class Meta:
        model = TransferTransferAttribute
        fields = ["id", "value", "name"]

class TransferFilterSerializer(serializers.ModelSerializer):
    user = UserFilterSerializer()
    attributes = PCTransferListAttributeFiltersSerializer(source="transfer_value", many=True)
    class Meta:
        model = PCTransfer
        fields = ["id", "transition_type", "created_at", 
                  "updated_at", "user", "excel_file", "attributes"]
        
class PalletCellTransferFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletCellTransfer
        fields = "__all__"

class TransferFilterFileSerializer(serializers.ModelSerializer):
    user = UserFilterSerializer()
    attributes = PCTransferListAttributeFiltersSerializer(source="transfer_value", many=True)
    transfers = PalletCellTransferFFileSerializer(source="transition_transfer", many=True)
    class Meta:
        model = PCTransfer
        fields = ["id", "transition_type", "created_at", 
                  "updated_at", "user", "excel_file", "attributes",
                  "transfers"]
        
class CellProductOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ["code"]

class UnitFPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"
        
class ProductFilterSerializer(serializers.ModelSerializer):
    cells = serializers.SerializerMethodField("getcells")
    unit = serializers.CharField(source="unit.title")
    amount = serializers.SerializerMethodField("getamount")
    class Meta:
        model = Product
        fields = ["id", "code", "title", "qrcode", "description",
                  "image", "price", "is_active", "created_at", 
                  "unit", "amount", "cells"]
        
    def getcells(self, obj):
        cells = Cell.objects.filter(product_id=obj, is_full=True)
        titles = []
        for cell in cells:
            titles.append(cell.code)
        return titles
    
    def getamount(self, obj):
        cells = Cell.objects.filter(product_id=obj, is_full=True)
        total_amount = 0
        for cell in cells:
            pallet = cell.pallet_id
            attributes = PalletPalletAttribute.objects.filter(pallet_id=pallet)
            for attr in attributes:
                if attr.pallet_attr_id.title == obj.unit.title:
                    total_amount = total_amount + attr.value

        return total_amount
    
class ProductStockAmountSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source="unit.title")
    amount = serializers.SerializerMethodField("getamount")
    class Meta:
        model = Product
        fields = ["id", "code", "title", "qrcode", "description", 
                  "image", "price", "is_active", "created_at", 
                  "updated_at", "unit", "amount"]
    
    def getamount(self, obj):
        cells = Cell.objects.filter(product_id=obj, is_full=True)
        total_amount = 0
        for cell in cells:
            pallet = cell.pallet_id
            attributes = PalletPalletAttribute.objects.filter(pallet_id=pallet)
            for attr in attributes:
                if attr.pallet_attr_id.title == obj.unit.title:
                    total_amount = total_amount + attr.value

        return total_amount