from rest_framework import serializers

from batch.models import (Batch, BatchAttribute, BatchBatchAttribute,
                          Container, ContainerAttribute, ContainerContainerAttribute,
                          Pallet, BatchContainer, PalletAttribute, 
                          PalletPalletAttribute)

from transfer.models import PCTransfer, PalletCellTransfer

from api.product.serializers import ProductDetailSerializer, ProductSimpleListSerializer
from product.models import (Product, Unit, ProductProductAttribute,
                            ProductAttribute)
from stock.models import Cell
from GlobalVariables import *

class CellFPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = "__all__"

class BatchAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchAttribute
        fields = "__all__"

class BBAttrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchBatchAttribute
        fields = "__all__"

class ContainerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"

class BBAttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="batch_batch_id.title")
    attr_id = serializers.IntegerField(source="batch_batch_id.id")
    class Meta:
        model = BatchBatchAttribute
        fields = ["id", "value", "name", "batch_id", "attr_id"]

class BatchListSerializer(serializers.ModelSerializer):
    attribute = BBAttributeSerializer(source="batch_value", many=True)
    class Meta:
        model = Batch
        fields = ["id", "title", "description", "arrived_at", "attribute"]

class BatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"

class ContainerAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerAttribute
        fields = "__all__"

class CntCntAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerContainerAttribute
        fields = "__all__"

class CCAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerContainerAttribute
        fields = "__all__"

class CCAttrOutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='container_attr_id.title')
    class Meta:
        model = ContainerContainerAttribute
        fields = ['id', 'value', 'container_id', 'name', 'container_attr_id']

class CCAttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="container_attr_id.title")
    attr_id = serializers.IntegerField(source="container_attr_id.id")
    class Meta:
        model = ContainerContainerAttribute
        fields = ["id", "name", "value", "attr_id"]

class PPAttrFBDSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="pallet_attr_id.title")
    attr_id = serializers.CharField(source="pallet_attr_id.id")
    class Meta:
        model = PalletPalletAttribute
        fields = ["id", "value", "name", "attr_id"]

class PalletCellTransferFPBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletCellTransfer
        fields = "__all__"

class PalletBatchSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(source="product_id")
    attributes = PPAttrFBDSerializer(source="pallet_attr_value", many=True)
    cell = CellFPDSerializer(source="cell_pallet")
    transfer_id = serializers.SerializerMethodField(method_name='gettransfer_id')
    transfer_price = serializers.SerializerMethodField(method_name='gettransfer_price')
    camera_id = serializers.SerializerMethodField(method_name='getcamera_id')

    class Meta:
        model = Pallet
        fields = ["id", "code", "title", "description", "product", "cell", 
                  "attributes", "transfer_id", "transfer_price", 'camera_id']
        
    def getcamera_id(self, obj):
        cell_id = Cell.objects.filter(pallet_id=obj).first()
        if cell_id:
            column_id = cell_id.column_id
            row_id = column_id.row_id
            camera_id = row_id.camera_id

            return camera_id.id
        else:
            return None
    
    def gettransfer_id(self, obj):
        queryset = PalletCellTransfer.objects.filter(pallet_id__id=obj.id, 
                                                     transfer_id__transition_type=INCOME).first()
        if queryset:
            return queryset.id
        return None
    
    def gettransfer_price(self, obj):
        queryset = PalletCellTransfer.objects.filter(pallet_id__id=obj.id, 
                                                     transfer_id__transition_type=INCOME).first()
         
        if queryset:
            return queryset.price
        return None

class ContainerListSerializer(serializers.ModelSerializer):
    attributes = CCAttributeSerializer(source="cnt_attr_value", many=True)
    pallets = PalletBatchSerializer(source="cnt_pallet", many=True)
    class Meta:
        model = Container
        fields = ["id", "title", "id_number", "type_code", "pallet_count",
                  "created_at", "updated_at", "attributes", "pallets"]

class PPAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletPalletAttribute
        fields = "__all__"

class ContainerSerializer(serializers.ModelSerializer):
    attributes = CCAttributeSerializer(source="cnt_attr_value", many=True)
    pallets = PalletBatchSerializer(source="cnt_pallet", many=True)
    class Meta:
        model = Container
        fields = ["id", "title", "id_number", "type_code", "pallet_count",
                  "created_at", "updated_at", "attributes", "pallets"]

class BatchContainerSerializer(serializers.ModelSerializer):
    info = ContainerSerializer(source="container_id")
    class Meta:
        model = BatchContainer
        fields = ["id", "info"]

class TransferFBDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCTransfer
        fields = "__all__"

class BatchDetailSerializer(serializers.ModelSerializer):
    attribute = BBAttributeSerializer(source="batch_value", many=True)
    containers = BatchContainerSerializer(source="batch_cnt", many=True)
    transfer_id = TransferFBDSerializer(source="transfer_batch")
    class Meta:
        model = Batch
        fields = ["id", "title", "description", "transfer_id", "arrived_at", "attribute", "containers"]

class BatchUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"

class BatchContainerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchContainer
        fields = "__all__"

class PalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"

class PalletCreateOutSerializer(serializers.ModelSerializer):
    product = ProductSimpleListSerializer(source="product_id")
    class Meta:
        model = Pallet
        fields = ["id", "code", "title", "description", "container_id", 
                  "product_id", "product"]

class ContainerAttributesSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="container_attr_id.id")
    name = serializers.CharField(source="container_attr_id.title")
    class Meta:
        model = ContainerContainerAttribute
        fields = ["id", "value", "name", "attr_id"]

class ContainerForPalletSerializer(serializers.ModelSerializer):
    attributes = ContainerAttributesSerializer(source="cnt_attr_value", many=True)
    class Meta:
        model = Container
        fields = ["id", "title", "id_number", "type_code", "pallet_count",
                  "created_at", "updated_at", "attributes"]

class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class ProductAttributesSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="product_attribute_id.id")
    name = serializers.CharField(source="product_attribute_id.title")
    class Meta:
        model = ProductProductAttribute
        fields = ["id", "value", "name", "attr_id"]

class ProductForPalletSerializer(serializers.ModelSerializer):
    attributes = ProductAttributesSerializer(source="product_attr_value", many=True)
    unit = ProductUnitSerializer()
    class Meta:
        model = Product
        fields = ["id", "code", "title", "qrcode", "description",
                  "image", "price", "is_active", "created_at",
                  "updated_at", "unit", "attributes"]

class PalletListSerializer(serializers.ModelSerializer):
    container = ContainerForPalletSerializer(source="container_id")
    product = ProductForPalletSerializer(source="product_id")
    class Meta:
        model = Pallet
        fields = ["id", "code", "title", "description", "container", "product"]

class PalletPalletAttributeSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="pallet_attr_id.id")
    name = serializers.CharField(source="pallet_attr_id.title")
    class Meta:
        model = PalletPalletAttribute
        fields = ["id", "value", "name", "attr_id"]

class PalletDetailSerializer(serializers.ModelSerializer):
    container = ContainerForPalletSerializer(source="container_id")
    product = ProductForPalletSerializer(source="product_id")
    attributes = PalletPalletAttributeSerializer(source="pallet_attr_value", many=True)
    cell = CellFPDSerializer(source="cell_pallet")
    class Meta:
        model = Pallet
        fields = ["id", "code", "title", "description", "attributes", "cell", "container", "product"]

class PalletAttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletAttribute
        fields = "__all__"

class PalletPAttrValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletPalletAttribute
        fields = "__all__"