from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.utils import talapnama_create, talapnama_create2

from api.utils import has_permission
from GlobalVariables import *
from .serializers import *
from transfer.models import *
from batch.models import PalletPalletAttribute

class PCTransferListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            operation_summary = "Transfer list, need to have Stock permission",
            responses = {200: PCTransferListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pc_transfers = PCTransfer.objects.all()
            results = self.paginate_queryset(pc_transfers, request, view=self)
            serializer = PCTransferListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data})
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PCTransferCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer create, need to have Stock and Manager permission",
        operation_description="***IMPORTANT*** 'transition_type' need to be 'Поступление' or 'Отправление'",
        request_body= PCTransferCreateSerilizer,
        responses = {200: PCTransferListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PCTransferCreateSerilizer(data=data)
            if serializer.is_valid():
                serializer.save()
                if PCTransfer.objects.filter(pk=serializer.data['id']).exists():
                    pctransfer_out = PCTransfer.objects.get(pk=serializer.data['id'])
                    serializer_out = PCTransferListSerializer(pctransfer_out)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                "detail":MSG_UNKNOWN_ERROR},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PCTransferDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer detail, need to have Stock permission",
        responses = {200: PCTransferDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if PCTransfer.objects.filter(pk=pk).exists():
                pctransfer = PCTransfer.objects.get(pk=pk)
                serializer = PCTransferDetailSerializer(pctransfer)
                return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PCTransferUDView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer update, need to have Stock and Manager permission",
        request_body = PCTransferCreateSerilizer,
        responses = {200: PCTransferListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PCTransfer.objects.filter(pk=pk).exists():
                pctransfer = PCTransfer.objects.get(pk=pk)
                serializer = PCTransferCreateSerilizer(pctransfer, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    pctransfer_out = PCTransfer.objects.get(pk=pk)
                    serializer_out = PCTransferListSerializer(pctransfer_out)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                            "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PCTransfer.objects.filter(pk=pk).exists():
                pctransfer = PCTransfer.objects.get(pk=pk)
                pctransfer.delete()
                return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class TransferAttributeListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            operation_summary = "Transfer attribute list, need to have Stock permission",
            responses = {200: TransferAttributeListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            tattributes = TransferAttribute.objects.all()
            serializer = TransferAttributeListSerializer(tattributes, many=True)
            return Response({"response":"success", "data": serializer.data})
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class TransferAttrCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer attribute create, need to have Stock and Manager permission",
        request_body= TransferAttributeListSerializer,
        responses = {200: TransferAttributeListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = TransferAttributeListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if TransferAttribute.objects.filter(pk=serializer.data['id']).exists():
                    transfer_attr = TransferAttribute.objects.get(pk=serializer.data['id'])
                    serializer_out = TransferAttributeListSerializer(transfer_attr)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                "detail":MSG_UNKNOWN_ERROR},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class TransferAttrUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer attribute update, need to have Stock and Manager permission",
        request_body= TransferAttributeListSerializer,
        responses = {200: TransferAttributeListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if TransferAttribute.objects.filter(pk=pk).exists():
                tattribute = TransferAttribute.objects.get(pk=pk)
                serializer = TransferAttributeListSerializer(tattribute, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                            "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class TTransferAttrCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer attribute value create, need to have Stock and Manager permission",
        request_body= TTransferAttrSerializer,
        responses = {200: TTransferAttrOutSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = TTransferAttrSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if TransferTransferAttribute.objects.filter(pk=serializer.data['id']).exists():
                    ttattribute = TransferTransferAttribute.objects.get(pk=serializer.data['id'])
                    serializer_out = TTransferAttrOutSerializer(ttattribute)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                "detail":MSG_UNKNOWN_ERROR},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class TTransferAttrUDView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Transfer attribute value update, need to have Stock and Manager permission",
        request_body= TTransferAttrSerializer,
        responses = {200: TTransferAttrOutSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if TransferTransferAttribute.objects.filter(pk=pk).exists():
                ttattribute = TransferTransferAttribute.objects.get(pk=pk)
                serializer = TTransferAttrSerializer(ttattribute, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    ttattribute_out = TransferTransferAttribute.objects.get(pk=pk)
                    serializer_out = TTransferAttrOutSerializer(ttattribute_out)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                            "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if TransferTransferAttribute.objects.filter(pk=pk).exists():
                ttattribute = TransferTransferAttribute.objects.get(pk=pk)
                ttattribute.delete()
                return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletCellTransferListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer List, need to have Stock permission", 
        responses = {200: PalletCellTransferListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pcc_transfer = PalletCellTransfer.objects.all()
            results = self.paginate_queryset(pcc_transfer, request, view=self)
            serializer = PalletCellTransferListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class PalletCellTransferCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
        request_body = PalletCellTransferCreateSerializer,
        responses = {200: PalletCellTransferListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletCellTransferCreateSerializer(data=data)
            if serializer.is_valid():
                if not Pallet.objects.filter(pk=data['pallet_id']).exists():
                    return Response({"response":"error", "err_code":ERR_PALLET_NOT_FOUND, 
                                "detail":MSG_PALLET_NOT_FOUND},
                                status=status.HTTP_400_BAD_REQUEST)
                if not Cell.objects.filter(pk=data['cell_id']).exists():
                    return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                "detail":MSG_CELL_NOT_FOUND},
                                status=status.HTTP_400_BAD_REQUEST)
                if not PCTransfer.objects.filter(pk=data['transfer_id']).exists():
                    return Response({"response":"error", "err_code":ERR_TRANSFER_NOT_FOUND, 
                                "detail":MSG_TRANSFER_NOT_FOUND},
                                status=status.HTTP_400_BAD_REQUEST)
                current_cell = Cell.objects.get(pk=data['cell_id'])
                current_transfer = PCTransfer.objects.get(pk=data['transfer_id'])
                current_pallet = Pallet.objects.get(pk=data['pallet_id'])

                column = current_cell.column_id
                row = column.row_id
                camera = row.camera_id
                if current_transfer.transition_type == INCOME:
                    if current_pallet.is_placed:
                        return Response({"response":"error", "err_code":ERR_PALLET_PLACED, 
                                    "detail":MSG_PALLET_PLACED},
                                    status=status.HTTP_400_BAD_REQUEST)
                    if current_cell.is_full:
                        return Response({"response":"error", "err_code":ERR_CELL_FULL, 
                                    "detail":MSG_CELL_NOT_EMPTY},
                                    status=status.HTTP_400_BAD_REQUEST)
                    current_cell.product_id = current_pallet.product_id
                    current_cell.is_full = True
                    current_cell.pallet_id = current_pallet
                    camera.empty_cells = camera.empty_cells - 1
                    current_pallet.is_sent = False
                    current_pallet.is_active = True
                    current_pallet.is_placed = True
                    current_pallet.save()
                    camera.save()
                    current_cell.save()
                if current_transfer.transition_type == OUTGO:
                    if not current_pallet.is_placed:
                        return Response({"response":"error", "err_code":ERR_PALLET_NOT_PLACED, 
                                    "detail":MSG_PALLET_NOT_PLACED},
                                    status=status.HTTP_400_BAD_REQUEST)
                    if not current_cell.is_full:
                        return Response({"response":"error", "err_code":ERR_CELL_EMPTY, 
                                    "detail":MSG_CELL_EMPYT},
                                    status=status.HTTP_400_BAD_REQUEST)
                    current_cell.product_id = None
                    current_cell.is_full = False
                    current_cell.pallet_id = None
                    camera.empty_cells = camera.empty_cells + 1
                    current_pallet.is_sent = True
                    current_pallet.save()
                    camera.save()
                    current_cell.save()
                serializer.save()
                talapnama_create(current_transfer.id)
                pcc_transfer_exists = PalletCellTransfer.objects.filter(pk=serializer.data['id']).exists()
                if pcc_transfer_exists:
                    pcc_transfer_out = PalletCellTransfer.objects.get(pk=serializer.data['id'])
                    serializer_out = PalletCellTransferListSerializer(pcc_transfer_out)
                    return Response({"response":"success", "data":serializer_out.data},
                                status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                "detail":MSG_UNKNOWN_ERROR},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        

class PalletCellTransferUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer update, need to have Stock and Manager permission",
        request_body = PalletCellTransferCreateSerializer,
        responses = {200: PalletCellTransferListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletCellTransfer.objects.filter(pk=pk).exists():
                data = request.data
                pctransfer = PalletCellTransfer.objects.get(pk=pk)
                serializer = PalletCellTransferCreateSerializer(pctransfer, data=data)
                if serializer.is_valid():
                    if not Pallet.objects.filter(pk=data['pallet_id']).exists():
                        return Response({"response":"error", "err_code":ERR_PALLET_NOT_FOUND, 
                                    "detail":MSG_PALLET_NOT_FOUND},
                                    status=status.HTTP_400_BAD_REQUEST)
                    if not Cell.objects.filter(pk=data['cell_id']).exists():
                        return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                    "detail":MSG_CELL_NOT_FOUND},
                                    status=status.HTTP_400_BAD_REQUEST)
                    if not PCTransfer.objects.filter(pk=data['transfer_id']).exists():
                        return Response({"response":"error", "err_code":ERR_TRANSFER_NOT_FOUND, 
                                    "detail":MSG_TRANSFER_NOT_FOUND},
                                    status=status.HTTP_400_BAD_REQUEST)
                    current_transfer = PCTransfer.objects.get(pk=data['transfer_id'])
                    old_transfer_id = pctransfer.transfer_id.id

                    if old_transfer_id != data['transfer_id']:
                        return Response({"response":"error", "err_code": ERR_WRONG_TRANSFER,
                                        "detail":MSG_WRONG_TRANSFER},
                                        status=status.HTTP_400_BAD_REQUEST)
                    
                    old_cell_id = pctransfer.cell_id.id
                    old_cell = Cell.objects.get(pk=old_cell_id)
                    old_column = old_cell.column_id
                    old_row = old_column.row_id
                    old_camera = old_row.camera_id

                    current_cell = Cell.objects.get(pk=data['cell_id'])
                    column = current_cell.column_id
                    row = column.row_id
                    camera = row.camera_id
                    current_pallet = Pallet.objects.get(pk=data['pallet_id'])
                    old_pallet = pctransfer.pallet_id

                    if current_transfer.transition_type == INCOME:
                        if old_pallet == current_pallet:
                            if old_cell == current_cell:
                                serializer.save()
                                pctransfer_out = PalletCellTransfer.objects.get(pk=pk)
                                serializer_out = PalletCellTransferListSerializer(pctransfer_out)
                                return Response({"response":"success", "data":serializer_out.data},
                                                status=status.HTTP_200_OK)
                            else:
                                old_cell.is_full = False
                                old_cell.product_id = None
                                old_cell.pallet_id = None
                                current_cell.is_full = True
                                current_cell.product_id = current_pallet.product_id
                                current_cell.pallet_id = current_pallet
                                if old_camera != camera:
                                    camera.empty_cells = camera.empty_cells - 1
                                    old_camera.empty_cells = old_camera.empty_cells + 1

                        else:
                            current_pallet.is_placed = True
                            old_pallet.is_placed = False
                            if old_cell == current_cell:
                                current_cell.product_id = current_pallet.product_id
                                current_cell.pallet_id = current_pallet
                                old_cell.product_id = current_pallet.product_id
                                old_cell.pallet_id = current_pallet

                            else:
                                old_cell.is_full = False
                                old_cell.product_id = None
                                old_cell.pallet_id = None
                                current_cell.product_id = current_pallet.product_id
                                current_cell.pallet_id = current_pallet
                                current_cell.is_full = True
                                if old_camera != camera:
                                    camera.empty_cells = camera.empty_cells - 1
                                    old_camera.empty_cells = old_camera.empty_cells + 1

                    if current_transfer.transition_type == OUTGO:
                        if old_pallet == current_pallet:
                            if old_cell == current_cell:
                                serializer.save()
                                pctransfer_out = PalletCellTransfer.objects.get(pk=pk)
                                serializer_out = PalletCellTransferListSerializer(pctransfer_out)
                                return Response({"response":"success", "data":serializer_out.data},
                                                status=status.HTTP_200_OK)
                            else:
                                old_cell.is_full = True
                                old_cell.product_id = old_pallet.product_id
                                old_cell.pallet_id = old_pallet
                                current_cell.is_full = False
                                current_cell.product_id = None
                                current_cell.pallet_id = None
                                if old_camera != camera:
                                    camera.empty_cells = camera.empty_cells + 1
                                    old_camera.empty_cells = old_camera.empty_cells - 1
                        else:
                            current_pallet.is_sent = True
                            old_pallet.is_sent = False
                            current_cell.product_id = None
                            current_cell.pallet_id = None
                            if old_cell == current_cell:
                                old_cell.product_id = None
                                old_cell.pallet_id = None
                            else:
                                old_cell.product_id = old_pallet.product_id
                                old_cell.pallet_id = old_pallet
                                old_cell.is_full = True
                                if old_camera != camera:
                                    camera.empty_cells = camera.empty_cells + 1
                                    old_camera.empty_cells = old_camera.empty_cells - 1
                    
                    old_cell.save()
                    old_pallet.save()
                    old_camera.save()
                    current_cell.save()
                    current_pallet.save()
                    camera.save()
                    serializer.save()
                    pctransfer_out = PalletCellTransfer.objects.get(pk=pk)
                    serializer_out = PalletCellTransferListSerializer(pctransfer_out)
                    talapnama_create(current_transfer.id)
                    return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                            "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
            

class PalletCellTransferDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer delete, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletCellTransfer.objects.filter(pk=pk).exists():
                pctransfer = PalletCellTransfer.objects.get(pk=pk)
                transfer_id = pctransfer.transfer_id
                cell = pctransfer.cell_id
                pallet = pctransfer.pallet_id
                column = cell.column_id
                row = column.row_id
                camera = row.camera_id

                if transfer_id.transition_type == INCOME:
                    cell.product_id= None
                    cell.pallet_id = None
                    cell.is_full = False
                    pallet.is_sent = False
                    pallet.is_placed = False
                    camera.empty_cells = camera.empty_cells + 1
                if transfer_id.transition_type == OUTGO:
                    cell.product_id= pallet.product_id
                    cell.pallet_id = pallet
                    cell.is_full = True
                    pallet.is_sent = False
                    pallet.is_placed = True
                    camera.empty_cells = camera.empty_cells - 1
                
                cell.save()
                pallet.save()
                camera.save()
                pctransfer.delete()
                return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletTransferPaginatedListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Transfer list, need to have Stock permission",
        responses = {200: PalletTransferListSerializer},
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pallet_transfer = PalletTransfer.objects.all()
            results = self.paginate_queryset(pallet_transfer, request, view=self)
            serializer = PalletTransferListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response": "success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletTransferCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
        request_body = PalletTransferCreateSerializer,
        responses = {200: PalletTransferDetailSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletTransferCreateSerializer(data=data)
            if serializer.is_valid():
                if not Cell.objects.filter(pk=data['out_cell_id']).exists():
                    return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                "detail":MSG_CELL_NOT_FOUND},
                                status=status.HTTP_400_BAD_REQUEST)
                if not Cell.objects.filter(pk=data['in_cell_id']).exists():
                    return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                "detail":MSG_CELL_NOT_FOUND},
                                status=status.HTTP_400_BAD_REQUEST)
                cell_out = Cell.objects.get(pk=data['out_cell_id'])
                cell_in = Cell.objects.get(pk=data['in_cell_id'])
                if not cell_out.is_full:
                    return Response({"response":"error", "err_code":ERR_CELL_EMPTY, 
                                    "detail":MSG_CELL_EMPYT},
                                    status=status.HTTP_400_BAD_REQUEST)
                if cell_in.is_full:
                    return Response({"response":"error", "err_code":ERR_CELL_FULL, 
                                    "detail":MSG_CELL_NOT_EMPTY},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                out_column = cell_out.column_id
                out_row = out_column.row_id
                out_camera = out_row.camera_id

                in_column = cell_in.column_id
                in_row = in_column.row_id
                in_camera = in_row.camera_id

                if out_camera.id != in_camera.id:
                    out_camera.empty_cells = out_camera.empty_cells + 1
                    in_camera.empty_cells = in_camera.empty_cells - 1
                    in_camera.save()
                    out_camera.save()

                cell_in.pallet_id = cell_out.pallet_id
                cell_in.product_id = cell_out.product_id
                cell_in.is_full = True
                cell_out.pallet_id = None
                cell_out.is_full = False
                cell_out.product_id = None

                cell_out.save()
                cell_in.save()
                serializer.save()

                if PalletTransfer.objects.filter(pk=serializer.data['id']).exists():
                    p_transfer_out = PalletTransfer.objects.get(pk=serializer.data['id'])
                    serializer_out = PalletTransferDetailSerializer(p_transfer_out)
                    return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                "detail":MSG_UNKNOWN_ERROR},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletTransferDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
        responses = {200: PalletTransferDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if PalletTransfer.objects.filter(pk=pk).exists():
                pallet_transfer = PalletTransfer.objects.get(pk=pk)
                serializer = PalletTransferDetailSerializer(pallet_transfer)
                return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    
class PalletTransferUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer update, need to have Stock and Manager permission",
        request_body = PalletTransferCreateSerializer,
        responses = {200: PalletTransferDetailSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletTransfer.objects.filter(pk=pk).exists():
                data = request.data
                pallet_transfer = PalletTransfer.objects.get(pk=pk)
                serializer = PalletTransferCreateSerializer(pallet_transfer, data=data)
                if serializer.is_valid():
                    if not Cell.objects.filter(pk=data['out_cell_id']).exists():
                        return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                    "detail":MSG_CELL_NOT_FOUND},
                                    status=status.HTTP_400_BAD_REQUEST)
                    if not Cell.objects.filter(pk=data['in_cell_id']).exists():
                        return Response({"response":"error", "err_code":ERR_CELL_NOT_FOUND, 
                                    "detail":MSG_CELL_NOT_FOUND},
                                    status=status.HTTP_400_BAD_REQUEST)
                    cell_out = Cell.objects.get(pk=data['out_cell_id'])
                    cell_in = Cell.objects.get(pk=data['in_cell_id'])
                    
                    
                    
                    cell_in_old = pallet_transfer.in_cell_id
                    cell_out_old = pallet_transfer.out_cell_id

                    out_column = cell_out.column_id
                    out_row = out_column.row_id
                    out_camera = out_row.camera_id

                    in_column = cell_in.column_id
                    in_row = in_column.row_id
                    in_camera = in_row.camera_id

                    in_column_old = cell_in_old.column_id
                    in_row_old = in_column_old.row_id
                    in_camera_old = in_row_old.camera_id

                    out_column_old = cell_out_old.column_id
                    out_row_old = out_column_old.row_id
                    out_camera_old = out_row_old.camera_id

                    if cell_out_old.id == cell_out.id:
                        if cell_in_old.id == cell_in.id:
                            serializer.save()
                            if PalletTransfer.objects.filter(pk=serializer.data['id']).exists():
                                p_transfer_out = PalletTransfer.objects.get(pk=serializer.data['id'])
                                serializer_out = PalletTransferDetailSerializer(p_transfer_out)
                                return Response({"response":"success", "data":serializer_out.data},
                                                status=status.HTTP_200_OK)
                            else:
                                return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                            "detail":MSG_UNKNOWN_ERROR},
                                            status=status.HTTP_404_NOT_FOUND)
                        else:
                            if cell_in.is_full:
                                return Response({"response":"error", "err_code":ERR_CELL_FULL, 
                                                "detail":MSG_CELL_NOT_EMPTY},
                                                status=status.HTTP_400_BAD_REQUEST)
                            cell_in.product_id = cell_in_old.product_id
                            cell_in.pallet_id = cell_in_old.pallet_id
                            cell_in.is_full = True
                            cell_in_old.is_full = False
                            cell_in_old.pallet_id = None
                            cell_in_old.product_id = None
                            cell_in_old.save()
                            cell_in.save()
                            if in_camera.id != in_camera_old:
                                in_camera_old.empty_cells = in_camera_old.empty_cells + 1
                                in_camera.empty_cells = in_camera.empty_cells - 1
                                in_camera.save()
                                in_camera_old.save()
                    else:
                        if out_camera.id != out_camera_old.id:
                            out_camera_old.empty_cells = out_camera_old.empty_cells - 1
                            out_camera.empty_cells = out_camera.empty_cells + 1
                            out_camera_old.save()
                            out_camera.save()
                        if cell_in_old.id == cell_in.id:
                            if not cell_out.is_full:
                                return Response({"response":"error", "err_code":ERR_CELL_EMPTY, 
                                                "detail":MSG_CELL_EMPYT},
                                                status=status.HTTP_400_BAD_REQUEST)
                            cell_out_old.product_id = cell_in.product_id
                            cell_out.product_id = None
                            cell_out_old.pallet_id = cell_in.pallet_id
                            cell_out.pallet_id = None
                            cell_out_old.is_full = True
                            cell_out.is_full = False

                            cell_out_old.save()
                            cell_out.save()
                        else:
                            if cell_in.is_full:
                                return Response({"response":"error", "err_code":ERR_CELL_FULL, 
                                                "detail":MSG_CELL_NOT_EMPTY},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if not cell_out.is_full:
                                return Response({"response":"error", "err_code":ERR_CELL_EMPTY, 
                                                "detail":MSG_CELL_EMPYT},
                                                status=status.HTTP_400_BAD_REQUEST)
                            cell_out_old.product_id = cell_in_old.product_id
                            cell_out_old.pallet_id = cell_in_old.pallet_id
                            cell_out_old.is_full = True
                            cell_in_old.is_full = False
                            cell_in_old.product_id = None
                            cell_in_old.pallet_id = None

                            cell_in.product_id = cell_out.product_id
                            cell_in.pallet_id = cell_out.pallet_id
                            cell_in.is_full = True
                            cell_out.product_id = None
                            cell_out.pallet_id = None
                            cell_out.is_full = False

                            cell_in_old.save()
                            cell_out_old.save()
                            cell_out.save()
                            cell_in.save()
                            if in_camera.id != in_camera_old:
                                in_camera_old.empty_cells = in_camera_old.empty_cells + 1
                                in_camera.empty_cells = in_camera.empty_cells - 1
                                in_camera.save()
                                in_camera_old.save()

                    serializer.save()
                    if PalletTransfer.objects.filter(pk=serializer.data['id']).exists():
                        p_transfer_out = PalletTransfer.objects.get(pk=serializer.data['id'])
                        serializer_out = PalletTransferDetailSerializer(p_transfer_out)
                        return Response({"response":"success", "data":serializer_out.data},
                                        status=status.HTTP_200_OK)
                    else:
                        return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                    "detail":MSG_UNKNOWN_ERROR},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                            "detail":MSG_PERMISSION_DECLINED},
                            status=status.HTTP_403_FORBIDDEN)
        
class PalletTransferDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Transfer delete, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletTransfer.objects.filter(pk=pk).exists():
                pallet_transfer = PalletTransfer.objects.get(pk=pk)
                cell_in_old = pallet_transfer.in_cell_id
                cell_out_old = pallet_transfer.out_cell_id


                out_column_old = cell_out_old.column_id
                out_row_old = out_column_old.row_id
                out_camera_old = out_row_old.camera_id

                out_camera_old.empty_cells = out_camera_old.empty_cells - 1
                out_camera_old.save()

                in_column_old = cell_in_old.column_id
                in_row_old = in_column_old.row_id
                in_camera_old = in_row_old.camera_id

                in_camera_old.empty_cells = in_camera_old.empty_cells + 1
                in_camera_old.save()

                cell_out_old.product_id = cell_in_old.product_id
                cell_out_old.pallet_id = cell_in_old.pallet_id
                cell_out_old.is_full = True
                cell_in_old.is_full = False
                cell_in_old.product_id = None
                cell_in_old.pallet_id = None


                cell_in_old.save()
                cell_out_old.save()
                pallet_transfer.delete()
                return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletReducePaginatedListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Reduce list, need to have Stock permission",
        responses = {200: PalletReduceListSerializer},
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pallet_reduce = PalletReduce.objects.all()
            results = self.paginate_queryset(pallet_reduce, request, view=self)
            serializer = PalletReduceListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response": "success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class PalletReduceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Reduce list, need to have Stock permission",
        responses = {200: PalletReduceDetailSerializer},
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if PalletReduce.objects.filter(pk=pk).exists():
                pallet_reduce = PalletReduce.objects.get(pk=pk)
                serializer = PalletReduceDetailSerializer(pallet_reduce)
                return Response({"response": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletReduceCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
        request_body = PalletReduceCreateSerializer,
        responses = {200: PalletReduceListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletReduceCreateSerializer(data=data)
            if serializer.is_valid():
                if Pallet.objects.filter(pk=data['pallet_id']).exists():
                    if PalletAttribute.objects.filter(pk=data['pallet_attribute_id']).exists():
                        current_pallet = Pallet.objects.get(pk=data['pallet_id'])
                        pallet_attr = PalletAttribute.objects.get(pk=data['pallet_attribute_id'])
                        pallet_attr_value_exists = PalletPalletAttribute.objects.filter(
                                        pallet_id=current_pallet, pallet_attr_id=pallet_attr).exists()
                        if pallet_attr_value_exists:
                            pallet_attr_value = PalletPalletAttribute.objects.filter(
                                        pallet_id=current_pallet, pallet_attr_id=pallet_attr).first()
                            try:
                                amount = float(data['amount'])
                                pallet_attr_value.value = pallet_attr_value.value - amount
                                pallet_attr_value.save()
                            except:
                                return Response({"response":"error"})
                            serializer.save()
                            if PalletReduce.objects.filter(pk=serializer.data['id']).exists():
                                pallet_reduce_out = PalletReduce.objects.get(pk=serializer.data['id'])
                                serializer_out = PalletReduceListSerializer(pallet_reduce_out)
                                return Response({"response":"success", "data":serializer_out.data},
                                                status=status.HTTP_200_OK)
                            else:
                                return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                            "detail":MSG_UNKNOWN_ERROR},
                                            status=status.HTTP_404_NOT_FOUND)
                        else:
                            return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                        "detail":MSG_PRODUCT_NOT_FOUND},
                                        status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                    "detail":MSG_PRODUCT_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                "detail":MSG_PRODUCT_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class PalletReduceUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
        request_body = PalletReduceCreateSerializer,
        responses = {200: PalletReduceListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletReduce.objects.filter(pk=pk).exists():
                data = request.data
                pallet_reduce = PalletReduce.objects.get(pk=pk)
                serializer = PalletReduceCreateSerializer(pallet_reduce, data=data)
                if serializer.is_valid():
                    old_amount = pallet_reduce.amount
                    old_pallet = pallet_reduce.pallet_id
                    old_attribute = pallet_reduce.pallet_attribute_id
                    pallet_attr_value = PalletPalletAttribute.objects.filter(
                                            pallet_id=old_pallet, pallet_attr_id=old_attribute).first()
                    pallet_attr_value.value = pallet_attr_value.value + old_amount
                    pallet_attr_value.save()
                    if Pallet.objects.filter(pk=data['pallet_id']).exists():
                        if PalletAttribute.objects.filter(pk=data['pallet_attribute_id']).exists():
                            current_pallet = Pallet.objects.get(pk=data['pallet_id'])
                            pallet_attr = PalletAttribute.objects.get(pk=data['pallet_attribute_id'])
                            pallet_attr_value_exists = PalletPalletAttribute.objects.filter(
                                            pallet_id=current_pallet, pallet_attr_id=pallet_attr).exists()
                            if pallet_attr_value_exists:
                                pallet_attr_value = PalletPalletAttribute.objects.filter(
                                            pallet_id=current_pallet, pallet_attr_id=pallet_attr).first()
                                try:
                                    amount = float(data['amount'])
                                    pallet_attr_value.value = pallet_attr_value.value - amount
                                    pallet_attr_value.save()
                                except:
                                    return Response({"response":"error"})
                                serializer.save()
                                if PalletReduce.objects.filter(pk=serializer.data['id']).exists():
                                    pallet_reduce_out = PalletReduce.objects.get(pk=serializer.data['id'])
                                    serializer_out = PalletReduceListSerializer(pallet_reduce_out)
                                    return Response({"response":"success", "data":serializer_out.data},
                                                    status=status.HTTP_200_OK)
                                else:
                                    return Response({"response":"error", "err_code":ERR_UNKNOW_ERROR, 
                                                "detail":MSG_UNKNOWN_ERROR},
                                                status=status.HTTP_404_NOT_FOUND)
                            else:
                                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                            "detail":MSG_PRODUCT_NOT_FOUND},
                                            status=status.HTTP_404_NOT_FOUND)
                        else:
                            return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                        "detail":MSG_PRODUCT_NOT_FOUND},
                                        status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                                    "detail":MSG_PRODUCT_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                    "detail":MSG_PARAMETERS_INSUFFICIENT},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                            "detail":MSG_PRODUCT_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletReduceDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet Cell Transfer create, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletReduce.objects.filter(pk=pk).exists():
                pallet_reduce = PalletReduce.objects.get(pk=pk)
                old_amount = pallet_reduce.amount
                old_pallet = pallet_reduce.pallet_id
                old_attribute = pallet_reduce.pallet_attribute_id
                pallet_attr_value = PalletPalletAttribute.objects.filter(
                                        pallet_id=old_pallet, pallet_attr_id=old_attribute).first()
                try:
                    pallet_attr_value.value = pallet_attr_value.value + old_amount
                    pallet_attr_value.save()
                except:
                    return Response({"response":"error"})
                pallet_reduce.delete()
                return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)