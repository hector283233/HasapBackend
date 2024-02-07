from django.db import models
from product.models import Product

class Batch(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    arrived_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Партия"
        verbose_name_plural = "Партии"
        ordering = ['-arrived_at']
        
        
class BatchAttribute(models.Model):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Аттрибют Партии"
        verbose_name_plural = "Аттрибюты Партии"
        
    
class BatchBatchAttribute(models.Model):
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="batch_value",
                                 verbose_name="Партия")
    batch_batch_id = models.ForeignKey(BatchAttribute, on_delete=models.CASCADE, 
                                       related_name="batch_attribute_value", verbose_name="Аттрибют")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Величина")
    
    def __str__(self):
        return str(self.batch_id) + " - " + str(self.batch_batch_id)
    
    class Meta:
        verbose_name = "Величина Аттрибюта Партии"
        verbose_name_plural = "Величины Аттрибютов Партии"
        unique_together = ('batch_id', 'batch_batch_id',)
        
class Container(models.Model):
    title = models.CharField(max_length=255, verbose_name="Имя")
    id_number = models.CharField(max_length=255, verbose_name="Номер", unique=True)
    type_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Код")
    pallet_count = models.IntegerField(default=0, verbose_name="Количество Паллетов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обнавлено в")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Кантейнер"
        verbose_name_plural = "Кантейнеры"
        
class ContainerAttribute(models.Model):
    title = models.CharField(max_length=255, verbose_name="Имя аттрибюта", unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Аттрибют Контейнера"
        verbose_name_plural = "Аттрибюты Контейнеров"
        
class ContainerContainerAttribute(models.Model):
    container_id = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="cnt_attr_value",
                                     verbose_name="Контейнер")
    container_attr_id = models.ForeignKey(ContainerAttribute, on_delete=models.CASCADE,
                                          related_name="attr_cnt_value", verbose_name="Аттрибют контейнера")
    value = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.container_id) + " - " + str(self.container_attr_id)
    
    class Meta:
        verbose_name = "Величина Аттрибюта Контейнера"
        verbose_name_plural = "Величины Аттрибюта Контейнера"
        unique_together = ('container_id', 'container_attr_id',)


class BatchContainer(models.Model):
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="batch_cnt",
                                 verbose_name="Партия")
    container_id = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="cnt_batch",
                                     verbose_name="Контейнер")
    
    def __str__(self):
        return str(self.batch_id) + " - " + str(self.container_id)
    
    class Meta:
        verbose_name = "Контейнер Партии"
        verbose_name_plural = "Контейнеры Партии"
        unique_together = ('batch_id', 'container_id',)
        
class Pallet(models.Model):
    code = models.CharField(max_length=64, verbose_name="Код паллета", unique=True)
    title = models.CharField(max_length=255, verbose_name="Имя", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Доп инфо")
    container_id = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="cnt_pallet",
                                     verbose_name="Контейнер")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_pallet",
                                   verbose_name="Продукт")
    is_placed = models.BooleanField(default=False, verbose_name="Разместен?")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлен?")
    
    def __str__(self):
        return str(self.code)
    
    class Meta:
        verbose_name = "Паллет"
        verbose_name_plural = "Паллеты"
        
class PalletAttribute(models.Model):
    title = models.CharField(max_length=255, verbose_name="Имя аттрибюта", unique=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Аттрибют Паллета"
        verbose_name_plural = "Аттрибюты Паллета"
        
class PalletPalletAttribute(models.Model):
    pallet_id = models.ForeignKey('Pallet', related_name='pallet_attr_value', on_delete=models.CASCADE,
                             verbose_name="Паллет")
    pallet_attr_id = models.ForeignKey('PalletAttribute', related_name="attr_pallet_value",
                                       on_delete=models.CASCADE, verbose_name="Палет Аттрибют")
    value = models.FloatField(default=0, verbose_name="Величина")
    
    def __str__(self):
        return str(self.pallet_id) + " - " + str(self.pallet_attr_id)
    
    class Meta:
        verbose_name = "Значение Аттрибютов Паллета"
        verbose_name_plural = "Значении Аттрибютов Паллетов"
        unique_together = ('pallet_id', 'pallet_attr_id',)