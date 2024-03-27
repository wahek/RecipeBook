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
        try:
            recipes = Recipe.objects.filter(author=request.user).order_by('-id')
        except TypeError:
            return redirect('login')
        recipes_del = recipes.filter(is_active=False)
        recipes = recipes.filter(is_active=True)
        context = {
            'user': request.user,
            'recipes': recipes,
            'recipes_del': recipes_del,
        }
        return render(request, self.template_name, context)


class ProfileByID(View):
    template_name = 'registration/profileID.html'

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_active=True)
            recipes = Recipe.objects.filter(author=user, is_active=True).order_by('-id')
        except TypeError:
            context = {'dont_exist': 'Такого пользователя не существует, или аккаунт удалён'}
            return render(request, self.template_name, context)
        context = {
            'user': user,
            'recipes': recipes,
        }
        return render(request, self.template_name, context)


class ProfileChange(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date']
    template_name = 'registration/change.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
