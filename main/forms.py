from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import Recipe, RecipeIngredient, Ingredient, RecipeRating, Category

User = get_user_model()


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
    ingredients = forms.ModelMultipleChoiceField(label=' ', queryset=Ingredient.objects.all(),
                                                 widget=FilteredSelectMultiple(Ingredient._meta.verbose_name_plural,
                                                                               False))
    categories = forms.ModelChoiceField(queryset=Category.objects.all().order_by('-id'), label='Категория',
                                        required=True,
                                        widget=forms.Select(), empty_label='Выберите категорию')
    name = forms.CharField(max_length=100, label="Название рецепта",
                           widget=forms.TextInput(
                               attrs={'class': 'short-input-form, w-100', 'placeholder': "Название рецепта"}))
    description = forms.CharField(max_length=500, label="Краткое описание", widget=forms.Textarea(
        attrs={'class': 'short-input-form, w-100', 'placeholder': "Описание рецепта"}))
    instructions = forms.CharField(label="Как готовить", widget=forms.Textarea(
        attrs={'class': 'short-input-form, w-100', 'placeholder': "Рецепт"}))
    img = forms.ImageField(label='Добавьте изображение', required=False)
    cooking_time = forms.IntegerField(label="Время приготовления (в минутах)", min_value=1, max_value=1000)

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'img', 'cooking_time', 'ingredients']


class RecipeAddIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RatingRecipeForm(forms.ModelForm):
    RATING_CHOICES = [(i, '') for i in range(1, 5 + 1)]
    rating = forms.ChoiceField(label='Оцените рецепт',
                               widget=forms.RadioSelect(attrs={'class': 'd-flex gap-3 position-relative'}),
                               choices=RATING_CHOICES, )

    class Meta:
        model = RecipeRating
        fields = ['rating']
