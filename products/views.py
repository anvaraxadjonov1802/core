from email.mime import image

from django.db.models.fields import return_None
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    print(product, 'Getga kirdi')
    return render(request, 'shop/product_detail.html', {'product': product})


# Buyurtma yaratish
@login_required
def create_order(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0 or quantity > product.stock:
            return render(request, 'shop/product_detail.html', {
                'product': product,
                'error': 'Invalid quantity or not enough stock available.'
            })

        # Buyurtma yaratish yoki mavjud buyurtmani olish
        customer = CustomUser.objects.get(id=request.user.id)
        Order.objects.create(product=product, quantity=quantity, customer=customer, status="Pending")

        # Mahsulotni zaxiradan kamaytirish
        product.stock -= quantity
        product.save()

        return redirect('user_orders')

    return render(request, 'shop/product_detail.html', {'product': product})


# Buyurtma tafsilotlari
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'shop/order_detail.html', {'order': order, 'quantity': order.quantity})


# Foydalanuvchi buyurtmalari ro‘yxati
@login_required
def user_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'shop/user_orders.html', {'orders': orders})


@login_required
def create_product(request):
    if request.user.is_staff:
        if request.method == 'POST':
            image = request.FILES.get('image')
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')

            Product.objects.create(name=name, description=description, price=price, stock=stock, image=image)
            return redirect('product_list')

    return render(request, 'shop/create_product.html')


@login_required
def delete_product(request, product_id):
    if request.user.is_staff:
        product = Product.objects.filter(id=product_id).first()
        product.delete()
        return redirect('product_list')


@login_required
def update_product(request, product_id):
    # Foydalanuvchi staff ekanligini tekshirish
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to update products.")
        return redirect('product_list')

    # Mahsulotni topish yoki 404 xatolikni ko'rsatish
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Ma'lumotlarni POST so'rovdan olish
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)

        # Agar rasm yuklangan bo'lsa, uni yangilash
        if request.FILES.get('image'):
            product.image = request.FILES['image']

        # Ma'lumotlarni saqlash
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('product_list')

    # GET so'rov uchun sahifani ko'rsatish
    return render(request, 'shop/update_product.html', {'product': product})


@login_required
def get_order(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def get_orders(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
        return render(request, 'shop/user_orders.html', {'orders': orders})


@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        return render(request, 'shop/admin_dashboard.html')


@login_required
def get_users_list(request):
    if request.user.is_staff:
        users = CustomUser.objects.all()
        return render(request, 'shop/user_list.html', {'users': users})


@login_required
def get_products(request):
    if request.user.is_staff:
        products = Product.objects.all()
        return render(request, 'shop/products.html', {'products': products})


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order.customer)
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        order.status = status
        order.save()
        return redirect('get_orders')
    return render(request, 'shop/update_order.html', {'order': order})
