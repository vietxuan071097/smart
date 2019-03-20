import datetime
from home import models

BILL_ID = 'BILL-ID'


class Cart:
    def __init__(self, request):
        bill_id = request.session.get(BILL_ID)
        if bill_id:
            try:
                bill = models.Bill.objects.get(id=bill_id, checked_out=False)
            except models.Bill.DoesNotExist:
                bill = self.new(request)
        else:
            bill = self.new(request)
        self.bill = bill

    def __iter__(self):
        for item in self.bill.item_set.all():
            yield item

    def new(self, request):
        bill = models.Bill.objects.create(creation_date=datetime.datetime.now())
        request.session[BILL_ID] = bill.id
        return bill

    def add(self, product_id, quantity=1):
        if models.Bill_detail.objects.filter(bill=self.bill, product=models.Product.objects.get(id=int(product_id))):
            t = models.Bill_detail.objects.get(bill=self.bill,
                                               product=models.Product.objects.get(id=int(product_id))).quantity
            models.Bill_detail.objects.filter(bill=self.bill,
                                              product=models.Product.objects.get(id=int(product_id))).update(
                quantity=t + 1)
        else:
            models.Bill_detail.objects.create(bill=self.bill, product=models.Product.objects.get(id=int(product_id)),
                                              quantity=quantity)

    def remove(self, product_id):
        models.Bill_detail.objects.filter(bill=self.bill,
                                          product=models.Product.objects.get(id=int(product_id))).delete()

    def update(self, product_id, quantity):
        models.Bill_detail.objects.filter(bill=self.bill,
                                          product=models.Product.objects.get(id=int(product_id))).update(
            quantity=quantity)

    def count(self):
        result = 0
        for item in models.Bill_detail.objects.filter(bill=self.bill):
            result += 1 * item.quantity
        return result

    def sum(self):
        result = 0
        for item in models.Bill_detail.objects.filter(bill=self.bill):
            result += item.total_price()
        return result

    def get_item(self):
        return models.Bill_detail.objects.filter(bill=self.bill)

    def clear(self):
        for item in models.Bill_detail.objects.filter(bill=self.bill):
            item.delete()

    def order(self, request, table):
        models.Bill.objects.filter(id=self.bill.id).update(table=models.Table.objects.get(name=table))
        self.bill = self.new(request)
