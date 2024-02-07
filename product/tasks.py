from .models import Product, ProductLog
from datetime import datetime, date
from stock.models import Cell
from batch.models import Pallet, PalletPalletAttribute
from transfer.models import PCTransfer, TransferTransferAttribute, PalletCellTransfer
import time
from datetime import timedelta
from GlobalVariables import *

def product_amount_count():
    today = date.today()
    starting = time.perf_counter()

    products = Product.objects.all()

    for product in products:
        total_amount = 0
        total_price = 0
        cells = Cell.objects.filter(product_id=product)
        for cell in cells:
            amount = 0
            pallet = cell.pallet_id
            
            attribute = PalletPalletAttribute.objects.filter(pallet_id=pallet, 
                                                              pallet_attr_id__title=product.unit.title).first()
            pallet_transfers = PalletCellTransfer.objects.filter(pallet_id=pallet,
                                                                 transfer_id__transition_type=INCOME).first()
            if attribute:
                amount = attribute.value
                total_amount = total_amount + amount
            if pallet_transfers:
                price = pallet_transfers.price
        
            total_price = total_price + (amount * price)

        product_log = ProductLog.objects.filter(product_id=product,
                                                 created_at=today)
        for log in product_log:
            print(today==log.created_at)
            print(type(today))
            print(type(log.created_at))
        print(product_log)
        print(product_log.count())
        if not product_log:
            ProductLog.objects.create(
                product_id = product,
                total_amount = total_amount,
                total_price = total_price,
                created_at = today,
            )

        else:
            product_log = product_log.first()
            product_log.product_id = product
            product_log.total_amount = total_amount
            product_log.total_price = total_price
            product_log.save()


            


    ending = time.perf_counter()
    print(f"funtion run in {ending - starting} seconds.")