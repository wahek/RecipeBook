from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from random import choices

from .forms import RecipeAddForm, RecipeAddIngredientsForm, RatingRecipeForm
from .models import Recipe, RecipeIngredient, Ingredient, RecipeRating

MAX_RATING = 5


class RecipeAddView(View):
    template_name = 'recipes/recipe_add.html'

    def get(self, request):
        form = RecipeAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RecipeAddForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            ingredients = form.cleaned_data['ingredients']
            for ingredient in ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient, )
            return redirect('ingredients_add', recipe_id=recipe.id)
        return render(request, self.template_name, {'form': form})


class RecipeAddIngredientsView(View):
    template_name = 'recipes/recipe_add_amount_ingr.html'
    model = RecipeIngredient
    form = RecipeAddIngredientsForm

    def get(self, request, recipe_id):
        ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
        ingredients_name = Ingredient.objects.all()
        context = {
            'recipe_id': recipe_id,
            'ingredients': ingredients,
            'ingredients_name': ingredients_name,
        }
        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        errors = {}
        for ingredient in RecipeIngredient.objects.filter(recipe_id=recipe_id):
            amount_field_name = f"amount_{ingredient.ingredient_id}"
            unit_field_name = f"unit_{ingredient.ingredient_id}"
            amount = request.POST.get(amount_field_name)
            unit = request.POST.get(unit_field_name)
            # Преобразуем введенное значение количества в целое число
            try:
                amount = int(amount)
            except (ValueError, TypeError):
                amount = None
            # Проверяем, что введенное значение соответствует допустимому диапазону
            if amount is not None and (amount < 1 or amount > 1000):
                errors[ingredient.ingredient.name] = "Количество должно быть от 1 до 1000."
            # Если введенное значение недопустимо, выбрасываем ValidationError
            if amount is None and ingredient.amount is None:
                errors[ingredient.ingredient.name] = "Введите корректное значение для количества."
            # Обновляем значение количества и единицы измерения для ингредиента
            if not errors:
                ingredient.amount = amount
                ingredient.unit = unit
                ingredient.save()
        if errors:
            # Возвращаем шаблон с сообщениями об ошибках и данными формы
            ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
            ingredients_name = Ingredient.objects.all()
            context = {
                'recipe_id': recipe_id,
                'ingredients': ingredients,
                'ingredients_name': ingredients_name,
                'errors': errors,
            }
            return render(request, self.template_name, context)
        # Если ошибок нет, перенаправляем пользователя
        return redirect('recipe', pk=recipe_id)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        recipes = Recipe.objects.all()
        try:
            choice_recipes = choices(recipes, k=5)
        except IndexError:
            choice_recipes = recipes
        count = [i + 1 for i in range(len(choice_recipes) - 1)]
        return render(request, self.template_name,
                      {'choice_recipes': choice_recipes, 'count': count})


class RecipesView(View):
    template_name = 'recipes/recipes.html'
    recipes_per_page = 10  # Количество рецептов на странице

    def get(self, request):
        recipes = Recipe.objects.all().order_by('view')

        # Создание объекта Paginator
        paginator = Paginator(recipes, self.recipes_per_page)

        # Получение номера страницы из запроса
        page_number = request.GET.get('page')
        try:
            recipes_page = paginator.page(page_number)
        except PageNotAnInteger:
            recipes_page = paginator.page(1)
        except EmptyPage:
            recipes_page = paginator.page(paginator.num_pages)

        context = {
            'recipes_page': recipes_page,
        }
        return render(request, self.template_name, context)


class RecipeView(View):
    template_name = 'recipes/recipe.html'
    form = RatingRecipeForm

    def get(self, request, pk):

        recipe = get_object_or_404(Recipe, id=pk)
        recipe.view += 1
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        rating = recipe.average_rating()
        full_star = int(rating)
        if rating - full_star > 0.3:
            half_star = 1
        else:
            half_star = 0
        empty_star = MAX_RATING - full_star - half_star
        context = {
            'max_rating': range(MAX_RATING),
            'recipe': recipe,
            'ingredients': ingredients,
            'recipe_rating': rating,
            'full_star': range(full_star),
            'half_star': range(half_star),
            'empty_star': range(empty_star),
            'form': self.form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            form = self.form(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                if RecipeRating.objects.filter(user=user, recipe=recipe).exists():
                    RecipeRating.objects.filter(user=user, recipe=recipe).update(rating=rating)
                else:
                    RecipeRating.objects.create(user=user, recipe=recipe, rating=rating)
                return redirect('recipe', pk=pk)
        else:
            return redirect('login')
        return redirect('recipe', pk=pk)

class RecipeCheckView(View):
    template_name = 'recipes/recipe_check.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        context = {
            'recipe': recipe,
            'ingredients': ingredients,
        }
        return render(request, self.template_name, context)


class RecipeUpdateView(View):
    template_name = 'recipes/recipe_update.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        form = RecipeAddForm(instance=recipe)
        context = {'form': form, 'recipe': recipe}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        form = RecipeAddForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe', pk=pk)
        context = {'form': form, 'recipe': recipe}
        return render(request, self.template_name, context)
