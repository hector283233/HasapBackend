from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils import has_permission
from GlobalVariables import *
from .serializers import *
from batch.models import *
from transfer.models import PCTransfer

class BatchListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary = "Batch list, need to have Stock permission",
            responses = {200: BatchListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            batches = Batch.objects.all()
            results = self.paginate_queryset(batches, request, view=self)
            serializer = BatchListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data})
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    @swagger_auto_schema(
            operation_summary = "Batch create, need to have Stock and Manager permission",
            request_body= BatchCreateSerializer,
            responses = {200: BatchListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = BatchCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                current_batch = Batch.objects.filter(pk=serializer.data['id']).first()
                PCTransfer.objects.create(
                    transition_type = INCOME,
                    user = user,
                    batch_id = current_batch
                )
                return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                    "detail":MSG_PARAMETERS_INSUFFICIENT},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class BatchDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Batch detail, need to have Stock permission",
        responses = {200: BatchDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if Batch.objects.filter(pk=pk).exists():
                batch = Batch.objects.get(pk=pk)
                serializer = BatchDetailSerializer(batch)
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

    @swagger_auto_schema(
        operation_summary = "Change batch info, need to have Stock and Manager permission",
        request_body = BatchUpdateSerializer,
        responses = {200: BatchDetailSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if Batch.objects.filter(pk=pk).exists():
                batch = Batch.objects.get(pk=pk)
                serializer = BatchUpdateSerializer(batch, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    batch_out = Batch.objects.get(pk=pk)
                    serializer_out = BatchDetailSerializer(batch_out)
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
        
class BatchAttributeListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Batch attribute list, need to have Stock permission",
        responses = {200: BatchAttributeSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            battributes = BatchAttribute.objects.all()
            serializer = BatchAttributeSerializer(battributes, many=True)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class BatchAttributeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Batch Attribute create, need to have Stock and Manager permission",
        request_body= BatchAttributeSerializer,
        responses = {200: BatchAttributeSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data=request.data
            serializer = BatchAttributeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class BatchAttributeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Batch Attribute update, need to have Stock and Manager permission",
        request_body= BatchAttributeSerializer,
        responses = {200: BatchAttributeSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if BatchAttribute.objects.filter(pk=pk).exists():
                batch_attr = BatchAttribute.objects.get(pk=pk)
                serializer = BatchAttributeSerializer(batch_attr, data=request.data)
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
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class BBAttrCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="'batch_batch_id' - This is batch attribute id.",
        operation_summary = "Batch attribute value create, need to have Stock and Manager permission",
        request_body = BBAttrCreateSerializer,
        responses = {200: BBAttrCreateSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = BBAttrCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                batch_out_exists = BatchBatchAttribute.objects.filter(pk=serializer.data['id']).exists()
                if batch_out_exists:
                    batch_out = BatchBatchAttribute.objects.get(pk=serializer.data['id'])
                    serializer_out = BBAttributeSerializer(batch_out)
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

class BBAttrUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="'batch_batch_id' - This is batch attribute id.",
        operation_summary = "Batch attribute value update, need to have Stock and Manager permission",
        request_body = BBAttrCreateSerializer,
        responses = {200: BBAttrCreateSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if BatchBatchAttribute.objects.filter(pk=pk).exists():
                bb_attr_value = BatchBatchAttribute.objects.get(pk=pk)
                serializer = BBAttrCreateSerializer(bb_attr_value, data=request.data)
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
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    
    @swagger_auto_schema(
        operation_summary = "Batch attribute value delete, need to have Stock and Manager permission"
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if BatchBatchAttribute.objects.filter(pk=pk).exists():
                bb_attr_value = BatchBatchAttribute.objects.get(pk=pk)
                bb_attr_value.delete()
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

        
class ContainerListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Container list, need to have Stock permission",
        responses = {200: ContainerListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            containers = Container.objects.all()
            results = self.paginate_queryset(containers, request, view=self)
            serializer = ContainerListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class ContainerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="'batch_batch_id' - This is batch attribute id.",
        operation_summary = "Container create, need to have Stock and Manager permission",
        request_body = ContainerCreateSerializer,
        responses = {200: ContainerListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = ContainerCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                container_exists = Container.objects.filter(pk=serializer.data['id']).exists()
                if container_exists:
                    container_out = Container.objects.get(pk=serializer.data['id'])
                    serializer_out = ContainerListSerializer(container_out)
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

class ContainerUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Container info update, need to have Stock and Manager permission",
        request_body = ContainerCreateSerializer,
        responses = {200: ContainerCreateSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if Container.objects.filter(pk=pk).exists():
                container = Container.objects.get(pk=pk)
                serializer = ContainerCreateSerializer(container, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    container_out = Container.objects.get(pk=pk)
                    serializer_out = ContainerListSerializer(container_out)
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
              
class CntAttrListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Container attribute list, need to have Stock permission",
        responses = {200: ContainerAttributeSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            cnt_attributes = ContainerAttribute.objects.all()
            serializer = ContainerAttributeSerializer(cnt_attributes, many=True)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class CntAttrCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Container attribute create, need to have Stock and Manager permission",
        request_body= ContainerAttributeSerializer,
        responses = {200: ContainerAttributeSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = ContainerAttributeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class CntAttrUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Update Container Attribute, need to have Stock and Manager permission",
        request_body= ContainerAttributeSerializer,
        responses = {200: ContainerAttributeSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if ContainerAttribute.objects.filter(pk=pk).exists():
                cnt_attr = ContainerAttribute.objects.get(pk=pk)
                serializer = ContainerAttributeSerializer(cnt_attr, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success",
                                     "data":serializer.data},
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
        
class CntCntAttrCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Container Attribute value create, need to have Stock and Manager permission",
        request_body= CntCntAttributeSerializer,
        responses = {200: CntCntAttributeSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = CntCntAttributeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                ccattr_exists = ContainerContainerAttribute.objects.filter(pk=serializer.data['id']).exists()
                if ccattr_exists:
                    ccattr_out = ContainerContainerAttribute.objects.get(pk=serializer.data['id'])
                    serializer_out = CCAttrOutSerializer(ccattr_out)
                return Response({"response":"success", "data": serializer_out.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class CntCntAttrUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Update Container Attribute value, need to have Stock and Manager permission",
        request_body= CntCntAttributeSerializer,
        responses = {200: CntCntAttributeSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if ContainerContainerAttribute.objects.filter(pk=pk).exists():
                cc_attr = ContainerContainerAttribute.objects.get(pk=pk)
                serializer = CntCntAttributeSerializer(cc_attr, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success",
                                     "data":serializer.data},
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
    
    @swagger_auto_schema(
        operation_summary = "Delete Container Attribute value, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if ContainerContainerAttribute.objects.filter(pk=pk).exists():
                cc_attr = ContainerContainerAttribute.objects.get(pk=pk)
                cc_attr.delete()
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
        
class BatchContainerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Create Batch Container, need to have Stock and Manager permission",
        request_body = BatchContainerCreateSerializer,
        responses = {200: BatchContainerCreateSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = BatchContainerCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                batch_out_exists = BatchContainer.objects.filter(pk=serializer.data['id']).exists()
                if batch_out_exists:
                    batch_container_out = BatchContainer.objects.get(pk=serializer.data['id'])
                    serializer_out = BatchContainerSerializer(batch_container_out)
                    return Response({"response":"success", "data": serializer_out.data},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                "detail":MSG_PARAMETERS_INSUFFICIENT},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class BatchContainerUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Update Batch Container, need to have Stock and Manager permission",
        request_body = BatchContainerCreateSerializer,
        responses = {200: BatchContainerCreateSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if BatchContainer.objects.filter(pk=pk).exists():
                batch_container = BatchContainer.objects.get(pk=pk)
                serializer = BatchContainerCreateSerializer(batch_container, 
                                                            data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success",
                                     "data":serializer.data},
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
    
    @swagger_auto_schema(
        operation_summary = "Delete Batch Container, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if BatchContainer.objects.filter(pk=pk).exists():
                batch_container = BatchContainer.objects.get(pk=pk)
                container = batch_container.container_id
                container.delete()
                batch_container.delete()
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

class PalletListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet list, need to have Stock permission",
        responses = {200: PalletCreateSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pallets = Pallet.objects.all()
            results = self.paginate_queryset(pallets, request, view=self)
            serializer = PalletCreateSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class PalletDetailedListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet list, need to have Stock permission",
        responses = {200: PalletListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pallets = Pallet.objects.all()
            results = self.paginate_queryset(pallets, request, view=self)
            serializer = PalletListSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet create, need to have Stock and Manager permission",
        request_body= PalletCreateSerializer,
        responses = {200: PalletCreateSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if Pallet.objects.filter(pk=serializer.data['id']).exists():
                    pallet_out = Pallet.objects.get(pk=serializer.data['id'])
                    serializer_out = PalletCreateOutSerializer(pallet_out)
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
        
class PalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet detail, need to have Stock permission",
        responses = {200: PalletDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if Pallet.objects.filter(pk=pk).exists():
                pallet = Pallet.objects.get(pk=pk)
                serializer = PalletDetailSerializer(pallet)
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
        
    @swagger_auto_schema(
        operation_summary = "Pallet create, need to have Stock and Manager permission",
        request_body= PalletCreateSerializer,
        responses = {200: PalletCreateSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if Pallet.objects.filter(pk=pk).exists():
                pallet = Pallet.objects.get(pk=pk)
                serializer = PalletCreateSerializer(pallet, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    pallet_out = Pallet.objects.get(pk=pk)
                    serializer_out = PalletDetailSerializer(pallet_out)
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
            if Pallet.objects.filter(pk=pk).exists():
                pallet = Pallet.objects.get(pk=pk)
                pallet.delete()
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
        
class PalletAttributeList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet attribute list, need to have Stock permission",
        responses = {200: PalletAttributeListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            pattributes = PalletAttribute.objects.all()
            serializer = PalletAttributeListSerializer(pattributes, many=True)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletAttributeCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet attribute create, need to have Stock and Manager permission",
        responses = {200: PalletAttributeListSerializer},
        request_body = PalletAttributeListSerializer
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletAttributeListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "err_code":ERR_PARAMETERS_INSUFFICIENT, 
                                    "detail":MSG_PARAMETERS_INSUFFICIENT},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class PalletAttributeUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Pallet attribute update, need to have Stock and Manager permission",
        responses = {200: PalletAttributeListSerializer},
        request_body = PalletAttributeListSerializer
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletAttribute.objects.filter(pk=pk).exists():
                pattribute = PalletAttribute.objects.get(pk=pk)
                serializer = PalletAttributeListSerializer(pattribute, data=request.data)
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
                             status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class PalletPAttributeCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary = "Pallet attribute value create, need to have Stock and Manager permission",
            request_body= PalletPAttrValueCreateSerializer,
            responses = {200: PalletPalletAttributeSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PalletPAttrValueCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                ppattr_exists = PalletPalletAttribute.objects.filter(pk=serializer.data['id']).exists()
                if ppattr_exists:
                    ppattr = PalletPalletAttribute.objects.get(pk=serializer.data['id'])
                    serializer_out = PalletPalletAttributeSerializer(ppattr)
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

class PalletPAttributeUDView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary = "Pallet attribute value update, need to have Stock and Manager permission",
            request_body= PalletPAttrValueCreateSerializer,
            responses = {200: PalletPalletAttributeSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            if PalletPalletAttribute.objects.filter(pk=pk).exists():
                pp_attr_value = PalletPalletAttribute.objects.get(pk=pk)
                serializer = PalletPAttrValueCreateSerializer(pp_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if PalletPalletAttribute.objects.filter(pk=pk).exists():
                        pp_attr_value_out = PalletPalletAttribute.objects.get(pk=pk)
                        serializer_out = PalletPalletAttributeSerializer(pp_attr_value_out)
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
    
    @swagger_auto_schema(
            operation_summary = "Pallet attribute value delete, need to have Stock and Manager permission",
    )
    def delete(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if PalletPalletAttribute.objects.filter(pk=pk).exists():
                pp_attr_value = PalletPalletAttribute.objects.get(pk=pk)
                pp_attr_value.delete()
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