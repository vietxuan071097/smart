from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from home import models

BILL_ID = 'BILL-ID'


def update_data():
    data = []
    bills = models.Bill.objects.all()
    for bill in bills:
        if not bill.finished:
            data.append({'id': bill.id, 'creation_date': bill.creation_date.strftime("%d-%m-%Y %H:%M:%S")})
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('manager', {
        'type': 'chat_message',
        'message': data
    })


class Cart:
    def __init__(self, request):
        bill_id = request.session.get(BILL_ID)
        if bill_id:
            try:
                bill = models.Bill.objects.get(id=bill_id, finished=False)
            except models.Bill.DoesNotExist:
                bill = self.new(request)
        else:
            bill = self.new(request)
        self.bill = bill
        self.request = request

    def __iter__(self):
        for item in self.bill.item_set.all():
            yield item

    def new(self, request):
        bill = models.Bill.objects.create(creation_date=timezone.now())
        request.session[BILL_ID] = bill.id
        return bill

    def add(self, product_id, quantity=1):
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

    def order(self):
        list_product = self.request.session['product']
        for product_id in list_product:
            self.add(product_id, list_product[product_id])
        method = self.request.session['method']
        if method == 'table':
            models.Bill.objects.filter(id=self.bill.id).update(order_method=False, table=models.Table.objects.get(
                name=self.request.session['table']))
        else:
            models.Bill.objects.filter(id=self.bill.id).update(
                order_method=True,
                address=self.request.session['address'],
                phone_number=self.request.session['phone_number'])
        if self.request.POST.get('pay') == 'card':
            models.Wallet.objects.filter(user=models.User.objects.get(username=self.request.user.username)).update(
                balance=models.Wallet.objects.get(
                    user=models.User.objects.get(username=self.request.user.username)).balance - int(
                    self.request.POST.get('sum')))
            models.Bill.objects.filter(id=self.bill.id).update(paid=True)

        data = list(models.Bill.objects.all().values('id', 'creation_date'))
        bills = models.Bill.objects.all()
        data = []
        for bill in bills:
            if not bill.finished:
                data.append({'id': bill.id, 'creation_date': bill.creation_date.strftime("%d-%m-%Y %H:%M:%S")})
        update_data()

    def new_bill(self, request):
        self.new(request)
        self.request.session['product']={}

    def checkout(self, request):
        pay = request.POST.get('pay')
        if pay == 'money':
            models.Bill.objects.filter(id=self.bill.id).update(order_method=False,
                                                               table=models.Table.objects.get(
                                                                   name=request.POST.get('table')))
        else:
            models.Bill.objects.filter(id=self.bill.id).update(checked_out=True)
            models.Wallet.objects.filter(bill=self.bill).update(
                balance=models.Wallet.objects.filter(bill=self.bill).balance - request.POST.get('sum'))
