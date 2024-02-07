from django.db import models
from datetime import datetime, date

today = date.today()

 # Модель для единиц измерений
class Unit(models.Model):
    title = models.CharField(max_length=255, verbose_name="Имя единицы", unique=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

# Модель для продуктов
class Product(models.Model):
    code = models.CharField(max_length=255, verbose_name="Код продукта", unique=True)
    title = models.CharField(max_length=255, verbose_name="Имя продукта", unique=True)
    qrcode = models.ImageField(("QR код"), upload_to = "qrcodes/", default="qrcodes/default.jpg")
    description = models.TextField(blank=True, null=True, verbose_name="Доп инфо продукта")
    image = models.ImageField(("Фото"), upload_to = "products/", default="products/default.jpg")
    price = models.FloatField(default=0, verbose_name="Цена")
    unit = models.ForeignKey('Unit', related_name='product_unit', on_delete=models.SET_NULL,
                             blank=True, null=True, verbose_name='Единица измерения')
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.code) + " - " + str(self.title)
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        
# Модель для количеств продуктов
class ProductUnit(models.Model):
    product_id = models.ForeignKey('Product', related_name='product_value', on_delete=models.CASCADE,
                                   verbose_name="Продукт")
    unit_id = models.ForeignKey('Unit', related_name='unit_value', on_delete=models.CASCADE,
                                verbose_name="Единицы измерения")
    quantity = models.FloatField(default=0, verbose_name="Количество")
    
    def __str__(self):
        return str(self.product_id) + str(self.quantity)
    
    class Meta:
        verbose_name = "Количество Продукта"
        verbose_name_plural = "Количество Продуктов"


# Модель для аттрибютов продукта
class ProductAttribute(models.Model):
    title = models.CharField(max_length=255, verbose_name="Имя аттрибюта", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Аттрибют продукта"
        verbose_name_plural = "Аттрибюты продуктов"


# Модель для значений аттрибютов продукта
class ProductProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_attr_value",
                                    verbose_name="Продукт")
    product_attribute_id = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,
                                    related_name="attr_attr_value", verbose_name="Аттрибют")
    value = models.FloatField(default=0, verbose_name="Значение")

    def __str__(self):
        return str(self.product_id) + " - " + str(self.product_attribute_id)

    class Meta:
        verbose_name = "Значение Аттрибюта продукта"
        verbose_name_plural = "Значении Аттрибютов продукта"
        unique_together = ('product_id', 'product_attribute_id',)

class ProductLog(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name="products_amount_log")
    total_amount = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    created_at = models.DateField()

    class Meta:
        ordering = ['-created_at']
