from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from .forms import UserFormRegistration, UserFormLogin


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            messages.error(request, 'Такой пользователь уже существует')
            return redirect('registration')
        except User.DoesNotExist:
            form = UserFormRegistration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('index')
    else:
        form = UserFormRegistration()
    return render(request, 'registration.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
        except User.DoesNotExist:
            return redirect('registration')
        form = UserFormLogin(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserFormLogin()
    return render(request, 'signin.html', {'form': form})
