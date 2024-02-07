from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils import has_permission
from user.models import *
from stock.models import (Camera, Cell)
from .serializers import (CameraListSerializer, ProductCellOutSerializer,
                          CameraDetailSerializer)

from GlobalVariables import *

class CameraListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses = {200: CameraListSerializer},
        operation_summary = "List Cameras, need to have Stock permission",
        operation_description = "Need to be authorized to make this request," \
            "\nand need to have STOCK permission"
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            cameras = Camera.objects.all()
            serializer = CameraListSerializer(cameras, many=True)
            return Response({'response':'success', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class CameraDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Camera detail, need to have Stock permission",
        responses = {200: CameraListSerializer},
        operation_description = "Need to be authorized to make this request," \
            "\nand need to have STOCK permission"
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if Camera.objects.filter(pk=pk).exists():
                camera = Camera.objects.get(pk=pk)
                serializer = CameraDetailSerializer(camera)
                return Response({"response":"success",
                                 "data": serializer.data},
                                 status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)


class CellDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Cell detail, need to have Stock permission",
        responses = {200: ProductCellOutSerializer},
        operation_description = "Need to be authorized to make this request," \
            "\nand need to have STOCK permission"
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if Cell.objects.filter(pk=pk).exists():
                current_cell = Cell.objects.get(pk=pk)
                serializer = ProductCellOutSerializer(current_cell)
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
            