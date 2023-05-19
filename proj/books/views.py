from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib.auth import authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CartAddProductForm, OrderCreateForm
from django.core.mail import send_mail, BadHeaderError
from .models import Item, OrderItem, Order, LastViewed
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

def admin_page(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'books/admin.html', context)

@login_required
def item_list(request):
    items = Item.objects.all()
    last_viewed_items = LastViewed.objects.filter(user=request.user).order_by('-viewed_at')[:5]
    return render(request, 'books/base.html', {'items': items, 'last_viewed_items': last_viewed_items})

def create_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        max_id = Item.objects.all().aggregate(Max('id'))['id__max']
        if max_id is None:
            new_id = 1
        else:
            new_id = max_id + 1
        Item.objects.create(id=new_id, name=name, description=description, price=price, image=image)
        return redirect('item_list')
    else:
        return render(request, 'books/create_item.html')

def update_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.image = request.FILES.get('image')
        item.__init__()
        return redirect('item_list')
    else:
        return render(request, 'books/update_item.html', {'item': item})

def delete_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponse('Item not found')
    item.delete()
    return redirect('admin_page')

def product_detail(request, name):
    item = get_object_or_404(Item, name=name)
    cart_product_form = CartAddProductForm()
    product_url = f"/product/{name}/"
    last_viewed, created = LastViewed.objects.get_or_create(user=request.user, item=item)
    last_viewed.viewed_at = timezone.now()
    last_viewed.save()
    return render(request, 'books/product_detail.html', {'item': item, 'product_url': product_url, 'cart_product_form': cart_product_form})

def search_results(request):
  query = request.GET.get('q')
  search = Item.objects.filter(
    Q(name__icontains=query) |
    Q(description__icontains=query)
  )
  context = {'search': search, 'query': query}
  return render(request, 'books/search.html', context)


@require_POST
def cart_add(request, name):
    cart = Cart(request)
    product = get_object_or_404(Item, name=name)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, name):
    cart = Cart(request)
    product = get_object_or_404(Item, name=name)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'books/cart_detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            messages.success(request, 'Your order has been created')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'books/order_create.html', {'form': form})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'books/order_detail.html', {'order': order})

@require_POST
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_status = 'отменен'
    order.save()
    return redirect('order_detail', order_id=order_id)

def order_purchase(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'books/order_purchase.html', {'order': order})

def order_payment(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.payment_status = 'оплачен'
        order.save()
        messages.success(request, f"Order {order_id} has been purchased!")
        return redirect(reverse('order_detail', kwargs={'order_id': order_id}))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.all()
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
    return render(request, 'books/profile.html', {'orders': orders})

def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            send_mail('Мечтать не вредно! 🥰 Подтвердите подписку', 'Мечта ближе, чем можно представить', '210107181@stu.sdu.edu.kz', [email])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return redirect('item_list')