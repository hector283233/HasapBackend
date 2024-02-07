from django.db import models

from batch.models import Pallet, PalletAttribute, Batch
from user.models import User
from stock.models import Cell
from product.models import Product
from GlobalVariables import *

PCT_TYPE = [
    (INCOME, INCOME),
    (OUTGO, OUTGO),
]

class PCTransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='pct_user_transfer',
                             verbose_name='Пользователь')
    transition_type = models.CharField(max_length=64, choices=PCT_TYPE,
                                       default=INCOME)
    batch_id = models.OneToOneField(Batch, on_delete=models.SET_NULL, 
                                 related_name="transfer_batch", verbose_name="Партия",
                                 blank=True, null=True)
    excel_file = models.FileField(upload_to="files/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обнавлено в")
    
    def __str__(self):
        return str(self.user) + " - " + str(self.transition_type)
    
    class Meta:
        verbose_name = 'Трансакция'
        verbose_name_plural = 'Трансакции'
        ordering = ['-created_at']

class TransferAttribute(models.Model):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Аттрибют Трансакции"
        verbose_name_plural = "Аттрибюты Трансакции"

class TransferTransferAttribute(models.Model):
    pctransfer_id = models.ForeignKey(PCTransfer, on_delete=models.CASCADE, related_name="transfer_value",
                                 verbose_name="Трансакция")
    pctransfer_attribute_id = models.ForeignKey(TransferAttribute, on_delete=models.CASCADE, 
                                       related_name="transfer_attribute_value", verbose_name="Аттрибют")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Величина")
    
    def __str__(self):
        return str(self.pctransfer_id) + " - " + str(self.pctransfer_attribute_id)
    
    class Meta:
        verbose_name = "Величина Аттрибюта Трансакции"
        verbose_name_plural = "Величины Аттрибютов Трансакции"
        unique_together = ('pctransfer_id', 'pctransfer_attribute_id',)
        
class PalletCellTransfer(models.Model):
    pallet_id = models.ForeignKey(Pallet, on_delete=models.CASCADE,
                                  related_name='pallet_transfer',
                                  verbose_name="Паллет")
    transfer_id = models.ForeignKey(PCTransfer, on_delete=models.CASCADE,
                                      related_name='transition_transfer',
                                      verbose_name='Трансакция')
    price = models.FloatField(default=0, verbose_name="Цена")
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE,
                                related_name='cell_transfer',
                                verbose_name='Ячейка')
    
    def __str__(self):
        return str(self.pallet_id) + ' - ' + str(self.cell_id)
    
    class Meta:
        verbose_name = 'Ячейка Трансакции'
        verbose_name_plural = 'Ячейки Трансакции'
        unique_together = ('pallet_id', 'transfer_id')
        
class PalletTransfer(models.Model):
    out_cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE,
                                    related_name='pct_out_cell',
                                    verbose_name='Исходящее Ячейка')
    in_cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE,
                                   related_name='pct_in_cell',
                                   verbose_name='Входящее Ячейка')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='p_user_transfer',
                             verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обнавлено в")
    
    def __str__(self):
        return str(self.out_cell_id) + " - " + str(self.in_cell_id)
    
    class Meta:
        verbose_name = "Перемещение Содержимых ячейки"
        verbose_name_plural = "Перемещении Содержимых ячеек"


class PalletReduce(models.Model):
    pallet_id = models.ForeignKey(Pallet, on_delete=models.CASCADE,
                                  related_name="pallet_reduce",
                                  verbose_name="Паллет")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_reduce',
                             verbose_name='Пользователь')
    pallet_attribute_id = models.ForeignKey(PalletAttribute, on_delete=models.CASCADE,
                                            related_name="reduce_attribute",
                                            verbose_name="Аттрибют паллета")
    price = models.FloatField(default=0, verbose_name="Цена")
    amount = models.FloatField(default=0, verbose_name="Количество")
    reason = models.CharField(max_length=255, verbose_name="Причина", 
                            default="Порча")
    image = models.ImageField("Фото", upload_to="reduce/", default="reduce/default.jpg",)
    description = models.TextField(blank=True, null=True,
                                verbose_name="Подробнее")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обнавлено в")
    
    def __str__(self):
        return str(self.pallet_id) + " - " + str(self.amount)
    
    class Meta:
        verbose_name = "Уменьшение в Паллете"
        verbose_name_plural = "Уменьшение в Паллетах"