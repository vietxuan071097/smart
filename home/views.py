from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.cart import Cart
from home.models import Product, Table, Cover
from home.forms import RegistrationForm
from .forms import AddProduct, AddProduct_Image


# Create your views here.
def index(request, search_key=None):
    if search_key:
        Data = {'products': Product.objects.filter(name__icontains=request.GET.get('search_key')),
                'count': Cart(request).count()}
    else:
        Data = {'products': Product.objects.all(), 'covers': Cover.objects.all(), 'count': Cart(request).count()}
    return render(request, 'home/index.html', Data)


def add(request):
    Cart(request).add(request.GET.get('product_id'))
    return HttpResponse(Cart(request).count())


def cart(request):
    Data = {'tables': Table.objects.all(), 'items': Cart(request).get_item(), 'sum': Cart(request).sum(),
            'count': Cart(request).count()}
    return render(request, 'home/cart.html', Data)


def detail(request, product_id):
    Data = {'product': Product.objects.get(id=product_id),
            'images': Product.objects.get(id=product_id).get_img_all(), 'count': Cart(request).count()}
    return render(request, 'home/detail.html', Data)


def search(request):
    if request.method == 'GET':
        return index(request, request.GET.get('search_key'))
    return HttpResponseRedirect('/')


def remove(request):
    Cart(request).remove(request.GET.get('product_id'))
    return HttpResponseRedirect('../cart/')


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


def success(request):
    if request.method == 'GET':
        Cart(request).order(request, request.GET.get('table'))
        return HttpResponse("Gọi món thành công")
    return HttpResponseRedirect('../cart/')


def add_product(request):
    # p = AddProduct()
    i = AddProduct_Image()
    return render(request, 'home/add-product.html', {'i':i})
