from rest_framework import serializers

from product.models import (Product, Unit, ProductAttribute, 
                            ProductProductAttribute)

class ProductSimpleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PPAttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product_attribute_id.title")
    attr_id = serializers.IntegerField(source="product_attribute_id.id")
    class Meta:
        model = ProductProductAttribute
        fields = ["name", "value", "id", "attr_id"]

class UOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"
        

class ProductDetailSerializer(serializers.ModelSerializer):
    attribute = PPAttributeSerializer(source="product_attr_value", many=True)
    unit = serializers.CharField(source='unit.title')
    class Meta:
        model = Product
        fields = ["id", "code", "title", "qrcode", "description", "image", 
                  "is_active", "price", "unit", 'attribute']   
        
class ProductDDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "code", "title", "qrcode", "description", 
                   "image", "is_active", "price", "unit"]

class UnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = "__all__"

class ProductProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProductAttribute
        fields= "__all__"

class ProductAttrOutSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="id", read_only=True)
    class Meta:
        model = ProductAttribute
        fields = ["id", "title", "attr_id"]

class PPAttrOutSerializer(serializers.ModelSerializer):
    attr_id = serializers.IntegerField(source="product_attribute_id.id", read_only=True)
    product_attribute_name = serializers.CharField(source="product_attribute_id.title", read_only=True)
    class Meta:
        model = ProductProductAttribute
        fields = ["id", "value", "product_id", "product_attribute_id", "attr_id", "product_attribute_name"]