from django.db import models
from product.models import Product
from .signals import delete_cell_signal
from django.db.models.deletion import Collector
from django.db import (router,)
from batch.models import Pallet
from datetime import datetime, date

# Модель Камеры
class Camera(models.Model):
    code = models.CharField(max_length=64, unique=True, verbose_name="Код камеры")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название Камеры")
    description = models.TextField(blank=True, null=True, verbose_name="Доп онфо о камере")
    position = models.IntegerField(default=0, verbose_name='Расположение')
    total_cells = models.IntegerField(default=0, verbose_name="Количество ячеек")
    empty_cells = models.IntegerField(default=0, verbose_name="Количество пустых ячеек")
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"
        ordering = ["position"]

# Модель Аттрибюта Камеры        
class CameraAttribute(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Имя атрибюта")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Аттрибют Камеры"
        verbose_name_plural = "Аттрибюты Камеры"

# Соединяющий Модель Аттрибюта и Камеры        
class CameraCameraAttribute(models.Model):
    camera_id = models.ForeignKey('Camera', related_name='camera_attribute', on_delete=models.CASCADE, 
                                  verbose_name="Камера")
    camera_attribute_id = models.ForeignKey('CameraAttribute', related_name='camera_camera_attribute', 
                                            on_delete=models.CASCADE, verbose_name="Аттрибют Камеры")
    value = models.FloatField(blank=True, null=True, verbose_name="Величина")
    
    def __str__(self):
        return str(self.camera_id) + str(self.camera_attribute_id)
    
    class Meta:
        verbose_name = "Значения Аттрюбютов Камеры"
        verbose_name_plural = "Значении Аттрюбютов Камеры"
        unique_together = ('camera_id', 'camera_attribute_id',)
    
# Модель рядов в Камере
class Row(models.Model):
    code = models.CharField(max_length=64, unique=True, verbose_name="Код ряда")
    position = models.IntegerField(default=0, verbose_name='Расположение')
    camera_id = models.ForeignKey('Camera', related_name='camera_row', on_delete=models.CASCADE,
                                  verbose_name="Камера")
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Ряд"
        verbose_name_plural = "Ряды"
        ordering = ["position"]

# Модель столбцов в ряде        
class Column(models.Model):
    code = models.CharField(max_length=64, unique=True, verbose_name="Код столбца")
    position = models.IntegerField(default=0, verbose_name='Расположение')
    row_id = models.ForeignKey('Row', related_name='row_column', on_delete=models.CASCADE,
                               verbose_name="Ряд")
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Столбец"
        verbose_name_plural = "Столбцы"
        ordering = ["position"]
        
# Модель ячеек в столбце
class Cell(models.Model):
    code = models.CharField(max_length=64, unique=True, verbose_name="Код ячейки")
    position = models.IntegerField(default=0, verbose_name='Расположение')
    column_id = models.ForeignKey('Column', related_name='column_cell', on_delete=models.CASCADE,
                               verbose_name="Столбец")
    product_id = models.ForeignKey(Product, related_name='cell_product', on_delete=models.CASCADE,
                                   verbose_name='Продукт', blank=True, null=True)
    is_full = models.BooleanField(default=False, verbose_name="Наполненный?")
    pallet_id = models.OneToOneField(Pallet, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name="cell_pallet",
                                  verbose_name="Паллет")
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Ячейка"
        verbose_name_plural = "Ячейки"
        ordering = ["position"]
        
    def save(self, *args, **kwargs):
        changed = False
        if not self.pk:
            row = self.column_id.row_id
            camera = row.camera_id
            camera.total_cells = camera.total_cells + 1
            camera.empty_cells = camera.empty_cells + 1
            camera.save()
            
        super(Cell, self).save(*args, **kwargs)
        today = date.today()
        cell_log = CellLog.objects.filter(cell_id=self, created_at=today).first()
        
        if cell_log:
            cell_log.pallet_id = self.pallet_id
            cell_log.product_id = self.product_id
            cell_log.is_full = self.is_full
            cell_log.save()
        else:
            CellLog.objects.create(
                cell_id = self,
                is_full = self.is_full,
                pallet_id = self.pallet_id,
                product_id = self.product_id,
                created_at = today
            )
    
    def delete(self, using=None, keep_parents=False):
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        if self.is_full:
            return

        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using, origin=self)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()
        
delete_cell_signal(Cell)

class CellLog(models.Model):
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='cell_cell_log')
    is_full = models.BooleanField(default=False)
    pallet_id = models.ForeignKey(Pallet, on_delete=models.CASCADE, 
                                  related_name='pallet_cell_log', blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                   related_name='product_cell_log', blank=True, null=True)
    created_at = models.DateField()

    def __str__(self):
        return str(self.cell_id)

    class Meta:
        ordering = ['-created_at']
    

class CellAttribute(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Имя атрибюта")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Аттрибют Ячейки"
        verbose_name_plural = "Аттрибюты Ячейки"
        
        
# Соединяющий Модель Аттрибюта и Ячейки        
class CellCellAttribute(models.Model):
    cell_id = models.ForeignKey(Cell, related_name='cell_attribute', on_delete=models.CASCADE, 
                                  verbose_name="Ячейка")
    cell_attribute_id = models.ForeignKey('CellAttribute', related_name='cell_cell_attribute', 
                                            on_delete=models.CASCADE, verbose_name="Аттрибют чейки")
    value = models.FloatField(blank=True, null=True, verbose_name="Величина")
    
    def __str__(self):
        return str(self.cell_id) + str(self.cell_attribute_id)
    
    class Meta:
        verbose_name = "Значения Аттрюбютов Ячейки"
        verbose_name_plural = "Значении Аттрюбютов Ячейки"
        unique_together = ('cell_id', 'cell_attribute_id',)