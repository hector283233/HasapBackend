from rest_framework import serializers

from api.product.serializers import PPAttributeSerializer
from api.batch.serializers import ContainerSerializer, PalletDetailSerializer
from api.stock.serializers import ProductCellOutSerializer

from transfer.models import *
from user.models import User
from batch.models import Pallet, Container, PalletAttribute
from stock.models import Cell
from product.models import Product, Unit

class PCTransferListAttributesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="pctransfer_attribute_id.title")
    class Meta:
        model = TransferTransferAttribute
        fields = ["id", "value", "name"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PCTransferListSerializer(serializers.ModelSerializer):
    attributes = PCTransferListAttributesSerializer(source="transfer_value", many=True)
    user = UserSerializer()
    class Meta:
        model = PCTransfer
        fields = ["id", "transition_type", "created_at", 
                  "updated_at", "user", "excel_file", "attributes"]

class PCTransferCreateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = PCTransfer
        fields = "__all__"

class PalletCellTransferSerializer(serializers.ModelSerializer):
    pallet = PalletDetailSerializer(source="pallet_id")
    cell = ProductCellOutSerializer(source="cell_id")
    class Meta:
        model = PalletCellTransfer
        fields = ["id", "price", "pallet", "cell"]

class PCTransferAttributesSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="pctransfer_attribute_id.id")
    name = serializers.CharField(source="pctransfer_attribute_id.title")
    class Meta:
        model = TransferTransferAttribute
        fields = ["id", "value", "name", "attr_id"]

class PCTransferDetailSerializer(serializers.ModelSerializer):
    attributes = PCTransferAttributesSerializer(
        source="transfer_value", many=True)
    pallet_transfers = PalletCellTransferSerializer(
        source="transition_transfer", many=True)
    user = UserSerializer()
    class Meta:
        model = PCTransfer
        fields = ["id", "transition_type", "created_at", "updated_at", 
                  "user", "excel_file", "attributes", "pallet_transfers"]
        
class TransferAttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferAttribute
        fields = "__all__"

class TTransferAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferTransferAttribute
        fields = "__all__"

class TTransferAttrOutSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="pctransfer_attribute_id.id")
    name = serializers.CharField(source="pctransfer_attribute_id.title")
    class Meta:
        model = TransferTransferAttribute
        fields = ["id", "value", "pctransfer_id", "attr_id", "name"]

class CellPCTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = "__all__"

class PalletPCTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"

class PalletCellTransferListSerializer(serializers.ModelSerializer):
    pallet = PalletPCTSerializer(source="pallet_id")
    cell = CellPCTSerializer(source="cell_id")
    transfer = PCTransferListSerializer(source="transfer_id")
    class Meta:
        model = PalletCellTransfer
        fields = ["id", "price", "pallet", "cell", "transfer"]

class PalletCellTransferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletCellTransfer
        fields = "__all__"

class PalletTransferListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    out_cell = CellPCTSerializer(source="out_cell_id")
    in_cell = CellPCTSerializer(source="in_cell_id")
    class Meta:
        model = PalletTransfer
        fields = ['id', "created_at", "updated_at", "out_cell", 
                  "in_cell", "user"]

class PalletTransferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletTransfer
        fields = "__all__"

class PalletTransferOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletTransfer
        fields = "__all__"

class PalletTransferDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    out_cell = ProductCellOutSerializer(source="out_cell_id")
    in_cell = ProductCellOutSerializer(source="in_cell_id")
    class Meta:
        model = PalletTransfer
        fields = ["id", "created_at", "updated_at", "out_cell",
                  "in_cell", "user"]
        
class PalletAttributeFPRLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletAttribute
        fields= "__all__"

class PalletReduceListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pallet = PalletPCTSerializer(source="pallet_id")
    attribute = PalletAttributeFPRLSerializer(source="pallet_attribute_id")
    class Meta:
        model = PalletReduce
        fields = ["id", "price", "amount", "reason", "image", "description", 
                  "created_at", "updated_at", "pallet", "user", "attribute"]

class PalletReduceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletReduce
        fields = "__all__"
        

class PalletFPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"

class PalletReduceDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pallet = PalletFPDSerializer(source="pallet_id")
    attribute = PalletAttributeFPRLSerializer(source="pallet_attribute_id")
    class Meta:
        model = PalletReduce
        fields = ["id", "price", "amount", "reason", "image", "description",
                  "created_at", "updated_at", "pallet", "user", "attribute"]