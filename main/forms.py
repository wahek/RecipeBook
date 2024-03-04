from django import forms
from .models import User, Recipe, RecipeCategory, RecipeIngredient, Category, Ingredient
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserFormRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'gender']


class UserFormChange(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'gender']


class UserFormLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['created_at', 'updated_at', 'view', 'is_active', 'author']
