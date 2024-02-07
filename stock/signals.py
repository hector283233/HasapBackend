from django.dispatch import receiver
from django.db.models.signals import pre_delete

def delete_cell_signal(Cell):
    @receiver(pre_delete, sender=Cell)
    def decrement_cell_count(sender, instance, **kwargs):
        camera = instance.column_id.row_id.camera_id
        camera.total_cells = camera.total_cells - 1
        camera.empty_cells = camera.empty_cells - 1
        camera.save()