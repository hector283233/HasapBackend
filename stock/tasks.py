from .models import Camera, Row, Column, Cell, CellLog
from datetime import datetime, date
import time

def schedule_test():
    today = date.today()
    starting = time.perf_counter()
    cameras = Camera.objects.all()
    for camera in cameras:
        rows = Row.objects.filter(camera_id=camera)
        for row in rows:
            columns = Column.objects.filter(row_id=row)
            for column in columns:
                cells = Cell.objects.filter(column_id=column)
                for cell in cells:
                    log = CellLog.objects.filter(cell_id=cell, created_at=today).first()

                    if not log:
                        CellLog.objects.create(
                            cell_id = cell,
                            is_full = cell.is_full,
                            pallet_id = cell.pallet_id,
                            product_id = cell.product_id,
                            created_at = today
                        )
    ending = time.perf_counter()
    print(f"funtion run in {ending - starting} seconds.")