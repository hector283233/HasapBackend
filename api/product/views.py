from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from api.utils import has_permission
from product.models import (Product, Unit, ProductAttribute, ProductProductAttribute)
from .serializers import *
from GlobalVariables import *

class ProductSimpleListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Product simple list, need to have Stock permission",
        responses = {200: ProductSimpleListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            products = Product.objects.filter(is_active=True)
            serializer = ProductSimpleListSerializer(products, many=True)
            return Response({"response":"success", "data": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)


class ProductListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Product list, need to have Stock permission",
        responses = {200: ProductDetailSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            products = Product.objects.filter(is_active=True)
            results = self.paginate_queryset(products, request, view=self)
            serializer = ProductDetailSerializer(results, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"response":"success", "data": response.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
            
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Product detail, need to have Stock permission",
        responses = {200: ProductDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if has_permission(user, STOCK):
            if Product.objects.filter(pk=pk).exists():
                product_out = Product.objects.get(pk=pk)
                serializer_out = ProductDetailSerializer(product_out)
                return Response({"response":"success", "data":serializer_out.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "err_code":ERR_PRODUCT_NOT_FOUND, 
                             "detail":MSG_PRODUCT_NOT_FOUND},
                             status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"response": "error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
    
class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    @swagger_auto_schema(
        operation_summary = "Create product, need to have Stock and Manager permission",
        request_body = ProductDDetailSerializer,
        responses = {200: ProductDetailSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = ProductDDetailSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product_out_exists = Product.objects.filter(pk=serializer.data['id']).exists()
                if product_out_exists:
                    product_out = Product.objects.get(pk=serializer.data['id'])
                    serializer_out = ProductDetailSerializer(product_out)
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
            
class ProductUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_summary = "Update product info, need to have Stock and Manager permission",
        request_body = ProductDDetailSerializer,
        responses = {200: ProductDetailSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if Product.objects.filter(pk=pk).exists():
                product = Product.objects.get(pk=pk)
                serializer = ProductDDetailSerializer(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    product_out = Product.objects.get(pk=pk)
                    serializer_out = ProductDetailSerializer(product_out)
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
    


class ProductUnitsList(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "List the units, need to have Stock permission",
        responses={200: UnitListSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            units = Unit.objects.all()
            serializer = UnitListSerializer(units, many=True)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)

class ProductUnitsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create product unit, need to have Stock and Manager permission",
        request_body=UnitListSerializer,
        responses={200: UnitListSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = UnitListSerializer(data=data)
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
        
class ProductUnitsUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update product unit, need to have Stock and Manager permission",
        request_body = UnitListSerializer,
        responses={200: UnitListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if Unit.objects.filter(pk=pk).exists():
                unit = Unit.objects.get(pk=pk)
                serializer = UnitListSerializer(unit, data=request.data)
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


class ProductAttributeListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "List product Attributes, need to have Stock permission",
        responses = {200: ProductAttributeSerializer}
    )
    def get(self, request):
        user = request.user
        if has_permission(user, STOCK):
            attributes = ProductAttribute.objects.all()
            serializer = ProductAttributeSerializer(attributes, many=True)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response":"error", "err_code":ERR_PERMISSION_DECLINED, 
                             "detail":MSG_PERMISSION_DECLINED},
                             status=status.HTTP_403_FORBIDDEN)
        
class ProductAttributeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Create product attribute, need to have Stock and Manager permission",
        request_body= ProductAttrOutSerializer,
        responses={200: ProductAttrOutSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = ProductAttrOutSerializer(data=data)
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

class ProductAttributeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Update product attribute, need to have Stock and Manager permission",
        request_body= ProductAttrOutSerializer,
        responses={200: ProductAttrOutSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if ProductAttribute.objects.filter(pk=pk).exists():
                data = request.data
                attribute = ProductAttribute.objects.get(pk=pk)
                serializer = ProductAttrOutSerializer(attribute, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
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
        
class PPAttributeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update product attribute value, need to have Stock and Manager permission",
        request_body = PPAttrOutSerializer,
        responses = {200: PPAttrOutSerializer}
    )
    def post(self, request):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            data = request.data
            serializer = PPAttrOutSerializer(data=data)
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

class PPAttributeUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update product attribute value, need to have Stock and Manager permission",
        request_body = PPAttrOutSerializer,
        responses = {200: PPAttrOutSerializer}
    )
    def put(self, request, pk):
        user = request.user
        if has_permission(user, STOCK) and has_permission(user, MANAGER):
            if ProductProductAttribute.objects.filter(pk=pk).exists():
                data = request.data
                ppattributes = ProductProductAttribute.objects.get(pk=pk)
                serializer = PPAttrOutSerializer(ppattributes, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
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
        
