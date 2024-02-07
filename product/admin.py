from django.contrib import admin

from .models import (Product, Unit, ProductAttribute, 
                     ProductProductAttribute, ProductLog)

class ProductAttributeInline(admin.TabularInline):
    model = ProductProductAttribute
    extra = 3

# Конфигурация админки продукта
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductAttributeInline]
    list_display = ("code", "title", "is_active")
    search_fields = ("code", "title")

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute)
admin.site.register(Unit)
admin.site.register(ProductLog)