from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from .forms import UserFormRegistration, UserFormLogin


def index(request):
    return render(request, 'index.html')


class UserFormRegistrationView:
    form_class = UserFormRegistration
    template_name = 'registration.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        return render(request, self.template_name, {'form': form})
