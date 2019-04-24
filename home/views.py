from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import render, redirect
from manager import views as manage_view

from chat.models import Conversation
from home.cart import Cart
from home.forms import RegistrationForm, NewProduct
from home.models import Product, Table, Cover, UserProfile, Wallet, Bill_detail, Bill


# Create your views here.
def index(request, search_key=None):
    if 'product' not in request.session:
        request.session['product'] = {}
    if search_key:
        Data = {'products': Product.objects.filter(name__icontains=search_key),
                'count': count(request)}
    else:
        Data = {'products': Product.objects.all(), 'covers': Cover.objects.all(), 'count': count(request)}

    # start: su ly chat
    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    conversations = Conversation.objects.filter(member__in=[session])
    if request.user.id != 1:
        if conversations.count() < 1:
            cs = Conversation.objects.create()
            cs.member.add(session)
        else:
            cs = conversations[0]
        for ss in Session.objects.all():
            session_data = ss.get_decoded()
            if session_data != {}:
                uid = session_data.get('_auth_user_id')
                if uid == '1' and ss not in cs.member.all():
                    cs.member.add(ss)
    Data["conversations"] = conversations
    Data["user_name"] = request.user
    Data["SID"] = request.session.session_key
    # end: su ly chat

    return render(request, 'home/index.html', Data)


def count(request):
    if 'product' not in request.session:
        return 0
    result = 0
    for item, val in request.session['product'].items():
        result += val
    return result


def add_product(request):
    product_id = request.GET.get('product_id')
    if product_id in request.session['product']:
        request.session['product'][product_id] += 1
    else:
        request.session['product'][product_id] = 1
    return HttpResponse(count(request))


def get_price(product_id):
    return Product.objects.get(id=product_id).price


def get_name(product_id):
    return Product.objects.get(id=product_id).name


def get_url(product_id):
    return Product.objects.get(id=product_id).img.url


def sum_price(request):
    result = 0
    if 'product' in request.session:
        for product_id in request.session['product']:
            result += request.session['product'][product_id] * get_price(product_id)
    return result


def get_product(request):
    items = {}
    if request.session.get('product'):
        for product in request.session['product']:
            item = {'name': get_name(product), 'price': get_price(product),
                    'quantity': request.session['product'][product],
                    'url': get_url(product), 'total_price': get_price(product) * request.session['product'][product]}
            items[product] = item
    return items


def get_method(request):
    return request.session.get('method')


def cart(request):
    Data = {'tables': Table.objects.all(), 'items': get_product(request), 'sum': sum_price(request),
            'count': count(request)}
    return render(request, 'home/cart.html', Data)


def detail(request, product_id):
    Data = {'product': Product.objects.get(id=product_id), 'count': count(request)}
    return render(request, 'home/detail.html', Data)


def search(request):
    return index(request, request.GET.get('search_key'))


def remove(request):
    product_id = request.GET.get('product_id')
    if product_id in request.session['product']:
        del request.session['product'][product_id]
    return cart(request)


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return render(request, 'home/register-success.html')
    return render(request, 'home/register.html', {'form': form})


def error(request):
    return render(request, 'home/error.html')


def pay(request):
    method = request.POST.get('method')
    if method == 'table':
        request.session['method'] = 'table'
        request.session['table'] = request.POST.get('table')
    else:
        request.session['method'] = 'address'
        request.session['address'] = request.POST.get('address')
        request.session['phone_number'] = request.POST.get('phone_number')
    if request.user.is_authenticated:
        money = Wallet.objects.get(user=User.objects.get(username=request.user.username)).balance
        return render(request, 'home/pay.html',
                      {'money': money, 'sum': sum_price(request), 'balance': money - sum_price(request)})
    return render(request, 'home/pay.html', {'sum': sum_price(request)})


def success(request):
    if request.method == 'POST':
        Cart(request).order()
    return render(request, 'home/success.html')


def new_bill(request):
    Cart(request).new_bill(request)
    return index(request)


def new_product(request):
    if request.method == 'POST':
        form = NewProduct(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
    f = NewProduct()
    return render(request, 'home/new-product.html', {'form': f})


def profile(request):
    data = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
    money = Wallet.objects.get(user=User.objects.get(username=request.user.username))
    return render(request, 'home/profile.html', {'data': data, 'money': money})


def bill_detail(request, id):
    Data = {'items': Bill_detail.objects.filter(bill=Bill.objects.get(id=id)), 'id': id}
    return render(request, 'home/bill-detail.html', Data)


def finish(request, id):
    Bill.objects.filter(id=id).update(finished=True)
    return redirect('../manager/')