from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
# Create your views here.


def login_view(request):
    user_name = request.POST.get('user_name', False)
    user_password = request.POST.get('password', False)
    if user_name and user_password:
        authenticated_user = authenticate(
            username=user_name, password=user_password)
        if authenticated_user:
            login(request, authenticated_user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, 'login.html', {
            'user_name': user_name, 'login_error': True})

    if User.objects.filter(username=user_name).exists():
        return render(request, 'login.html', {'user_name': user_name})
    return render(request, 'registration.html', {'user_name': user_name})


def start_view(request):
    return render(request, 'start.html')


def registration_view(request):
    user_name = request.POST.get('user_name', False)
    user_password = request.POST.get('password', False)
    if user_name and user_password:
        user = User.objects.create_user(username=user_name,
                                        # email='jlennon@beatles.com',
                                        password=user_password)
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return redirect('login_endpoint')
