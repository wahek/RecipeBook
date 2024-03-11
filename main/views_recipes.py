from django.shortcuts import render, redirect
from django.views import View
from .forms import RecipeIngredientForm, RecipeAddForm


class RecipeAddView(View):
    template_name = 'recipes/recipe_add.html'

    def get(self, request):
        context = {
            'form_recipe': RecipeAddForm(),
            'form_ingredient': RecipeIngredientForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_recipe = RecipeAddForm(request.POST)
        form_ingredient = RecipeIngredientForm(request.POST)
        if form_recipe.is_valid() and form_ingredient.is_valid():
            form_recipe.save()
            form_ingredient.save()
            return redirect('index')
        context = {
            'form_recipe': form_recipe,
            'form_ingredient': form_ingredient
        }
        return render(request, self.template_name, context)


def test(request):
    form = RecipeAddForm(),
    return render(request, 'test.html')
