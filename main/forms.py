from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import Recipe, RecipeIngredient, Ingredient

User = get_user_model()


# class UserAuthenticationForm(AuthenticationForm, forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'email', }),
    )
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'birth_date')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'email', }),
    )
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'birth_date')


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeAddForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    linked_bars = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=FilteredSelectMultiple(Ingredient._meta.verbose_name_plural,
                                                                               False))

    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'description', 'instructions', 'linked_bars', 'img']


class RecipeAddIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'
