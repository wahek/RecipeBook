from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import render, redirect
from django.views import View
from .models import User, Recipe, RecipeRating


class Registration(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class Profile(View):
    template_name = 'registration/profile.html'

    def get(self, request):
        context = {
            'user': request.user,
            'recipes': Recipe.objects.filter(author=request.user)
        }
        return render(request, self.template_name, context)


class ProfileChange(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date']
    template_name = 'registration/change.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
