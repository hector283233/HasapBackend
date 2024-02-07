from django.contrib import admin

from .models import (Batch, BatchAttribute, BatchBatchAttribute, Container, 
                     ContainerAttribute, ContainerContainerAttribute, BatchContainer,
                     Pallet, PalletAttribute, PalletPalletAttribute)

class BatchAttributeInline(admin.TabularInline):
    model = BatchBatchAttribute
    extra = 3

class BatchAdmin(admin.ModelAdmin):
    model = Batch
    inlines = [BatchAttributeInline]
    list_display = ['title', 'arrived_at']
    search_fields = ('title', )

class ContainerAttributeInline(admin.TabularInline):
    model = ContainerContainerAttribute
    extra = 3

class ContainerAdmin(admin.ModelAdmin):
    model = Container
    inlines = [ContainerAttributeInline]
    list_display = ['title', 'id_number', 'type_code']
    search_fields = ('title', 'id_number', 'type_code')

class PalletAttributeInline(admin.TabularInline):
    model = PalletPalletAttribute
    extra = 3

class PalletAdmin(admin.ModelAdmin):
    model = Pallet
    inlines = [PalletAttributeInline]

admin.site.register(Batch, BatchAdmin)
admin.site.register(BatchAttribute)
admin.site.register(Container, ContainerAdmin)
admin.site.register(ContainerAttribute)
admin.site.register(ContainerContainerAttribute)
admin.site.register(BatchContainer)
admin.site.register(Pallet, PalletAdmin)
admin.site.register(PalletAttribute)