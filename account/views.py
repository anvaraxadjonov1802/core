from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser


def log_in(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'auth/login.html', {
                'error_message': "⚠️ Ma'lumotlar noto'g'ri kiritildi. Iltimos, qayta urinib ko'ring ❗️"
            })
    return render(
        request=request,
        template_name='auth/login.html'
    )
    
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        ex_user = CustomUser.objects.filter(phone_number=phone_number).first()

        if ex_user:
            return render(request, 'auth/signup.html', {
                'error_message': "⚠️ Bu telefon raqamdan foydalanuvchi ro'yhatdan o'tgan ❗️"
            })
        elif password1 != password2:
            return render(request, 'auth/signup.html', {
                'error_message': "⚠️ Parollar mos emas ❗️"
            })
        else:
            user = CustomUser.objects.create_user(
                name=name,
                phone_number=phone_number,
                password=password1
            )
            login(request=request, user=user)
            return redirect('product_list')

    return render(
        request=request,
        template_name='auth/signup.html'
    )

def log_out(request):
    print(request.user.is_authenticated)  # Foydalanuvchini autentifikatsiyasini tekshirish
    if request.user.is_authenticated:
        logout(request)  # Foydalanuvchini chiqish qilamiz
        return redirect('log_in')  # Login sahifasiga yo'naltiramiz
    return redirect('log_in')