from django.contrib import admin

from .models import (Camera, CameraAttribute, CameraCameraAttribute, 
                     Row, Column, Cell, CellAttribute, CellCellAttribute,
                     CellLog)


class CameraAttributeInline(admin.TabularInline):
    model = CameraCameraAttribute
    extra = 3

# Конфигурация админки Камеры
class CameraAdmin(admin.ModelAdmin):
    model=Camera
    inlines = [CameraAttributeInline]
    # readonly_fields = ("total_cells", "empty_cells", )
    list_display = ("code", "title", "total_cells", "empty_cells")
    search_fields = ("code", "title", "total_cells", "empty_cells")
    
class CellAttributeInline(admin.TabularInline):
    model = CellCellAttribute
    extra = 3
    
# Конфигурация админки Ячейки
class CellAdmin(admin.ModelAdmin):
    model = Cell
    inlines = [CellAttributeInline]
    list_display = ["code", "is_full"]
    search_fields = ("code", )
    actions = None


admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraAttribute)
admin.site.register(Row)
admin.site.register(Column)
admin.site.register(Cell, CellAdmin)
admin.site.register(CellAttribute)
admin.site.register(CellLog)