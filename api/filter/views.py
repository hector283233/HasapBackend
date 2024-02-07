from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils import (has_permission, validate_date, product_report, 
                       transfer_report, product_report2, transfer_report2)
from user.models import *
from batch.models import *
from product.models import *
from transfer.models import *
from stock.models import *

from GlobalVariables import *
import pandas as pd

from .serializers import *
from api.product.serializers import ProductSimpleListSerializer

class CellLogList(APIView):
    def get(self, request):
        logs = CellLog.objects.all()
        serailizer = CellLogSerializer(logs, many=True)
        return Response(serailizer.data)

class BatchFilterView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    startdate = openapi.Parameter("startdate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    enddate = openapi.Parameter("enddate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
            manual_parameters=[title, startdate, enddate],
            operation_description="***IMPORTANT*** date format need to be 'YYYY-MM-DD'",
            responses={200: BatchFilterSerializer},
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            title = request.query_params.get("title", None)
            startdate = request.query_params.get("startdate", None)
            enddate = request.query_params.get("enddate", None)
            if title:
                batches = Batch.objects.filter(title__icontains=title)
            else:
                batches = Batch.objects.all()
            if startdate and enddate:
                if validate_date(startdate) and validate_date(enddate):
                    batches = batches.filter(arrived_at__range=[startdate, enddate])
            
            results = self.paginate_queryset(batches, request, view=self)
            serializer = BatchFilterSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data":response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class TransferFilterView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    
    startdate = openapi.Parameter("startdate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    enddate = openapi.Parameter("enddate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
            manual_parameters=[startdate, enddate, user],
            operation_description="***IMPORTANT*** date format need to be 'YYYY-MM-DD'\n'user' paramter need to be Integer, id of user",
            responses={200: TransferFilterSerializer},
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            transfers = PCTransfer.objects.all()
            startdate = request.query_params.get("startdate", None)
            enddate = request.query_params.get("enddate", None)
            user = request.query_params.get("user", None)
            if startdate and enddate:
                if validate_date(startdate) and validate_date(enddate):
                    transfers = transfers.filter(created_at__range=[startdate, enddate])
            if user:
                transfers = transfers.filter(user__id=user)
            file_serializer = TransferFilterSerializer(transfers, many=True)
            # file = transfer_report(file_serializer.data)
            file = transfer_report2(startdate, enddate)
            results = self.paginate_queryset(transfers, request, view=self)
            serializer = TransferFilterSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data":response.data, "file":file},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class ProductFilterView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    code = openapi.Parameter("code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    minprice = openapi.Parameter("minprice", in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER)
    maxprice = openapi.Parameter("maxprice", in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER)
    @swagger_auto_schema(
            manual_parameters=[title, code, minprice, maxprice],
            operation_description="***IMPORTANT*** date format need to be 'YYYY-MM-DD'\n'user' paramter need to be Integer, id of user",
            responses={200: ProductFilterSerializer},
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            title = request.query_params.get("title", None)
            code = request.query_params.get("code", None)
            minprice = request.query_params.get("minprice", None)
            maxprice = request.query_params.get("maxprice", None)
            if title:
                products = Product.objects.filter(is_active=True, title__icontains=title)
            else:
                products = Product.objects.filter(is_active=True)
            if code:
                products = products.filter(code__icontains=code)
            if minprice and maxprice:
                products = products.filter(price__range=[minprice, maxprice])
            # file_serializer = ProductFilterSerializer(products, many=True)
            # file = product_report(file_serializer.data)
            file = product_report2(products)
            results = self.paginate_queryset(products, request, view=self)
            serializer = ProductFilterSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data":response.data, "file":file},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        

class CreateCellsView(APIView):

    def get(self, request):
        camera_id = request.query_params.get("camera_id", None)
        cell_qty = request.query_params.get("cell_qty", None)
        camera_id = int(camera_id)
        cell_qty = int(cell_qty)
        if camera_id and cell_qty:
            if Camera.objects.filter(pk=camera_id).exists():
                current_camera = Camera.objects.get(pk=camera_id)
                rows = Row.objects.filter(camera_id=current_camera)
                for row in rows:
                    columns = Column.objects.filter(row_id=row)
                    for column in columns:
                        print(column)
                        for i in range(1,cell_qty+1):
                            Cell.objects.create(
                                code=str(column.code) + ".Y"+str(i),
                                position = i,
                                column_id = column
                            )
        return Response("success")
    
class CreateCameraCells(APIView):

    def get(self, request):
        try:
            camera_id = request.query_params.get("camera_id", None)
            rows = request.query_params.get("rows", None)
            columns = request.query_params.get("columns", None)
            cells = request.query_params.get("cells", None)
            
            camera_id = int(camera_id)
            rows = int(rows)
            columns = int(columns)
            cells = int(cells)

            if camera_id and rows and columns and cells:
                if Camera.objects.filter(pk=camera_id).exists():
                    current_camera = Camera.objects.get(pk=camera_id)
                    
                    for i in range(1, rows + 1):
                        Row.objects.create(
                            code = str(current_camera.code) + ".X" + str(i),
                            position = i,
                            camera_id = current_camera
                        )
                    
                    current_rows = Row.objects.filter(camera_id=current_camera)

                    for row in current_rows:
                        for i in range(1, columns + 1):
                            Column.objects.create(
                                code = str(row.code) + ".Z" + str(i),
                                position = i,
                                row_id = row
                            )
                    
                    for row in current_rows:
                        current_columns = Column.objects.filter(row_id=row)
                        for column in current_columns:
                            for i in range(1, cells + 1):
                                Cell.objects.create(
                                    code = str(column.code) + ".Y" + str(i),
                                    position = i,
                                    column_id = column
                                )
            
            return Response("success")
        except:
            return Response("error")
        
class DeleteColumnCells(APIView):
    def delete(self, request):
        logs = CellLog.objects.all()
        for log in logs:
            log.delete()
        return Response("Success")