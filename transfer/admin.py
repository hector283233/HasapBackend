from django.contrib import admin

from .models import (PCTransfer, PalletCellTransfer, PalletTransfer,
                     PalletReduce, TransferAttribute, TransferTransferAttribute)

class PalletCellTransferInline(admin.TabularInline):
    model = PalletCellTransfer
    extra = 3

class TTAttributeAdmin(admin.TabularInline):
    model = TransferTransferAttribute
    extra = 3
    
class TransferAdmin(admin.ModelAdmin):
    model = PCTransfer
    inlines = [PalletCellTransferInline, TTAttributeAdmin]

admin.site.register(PCTransfer, TransferAdmin)
admin.site.register(PalletCellTransfer)
admin.site.register(PalletTransfer)
admin.site.register(PalletReduce)
admin.site.register(TransferAttribute)