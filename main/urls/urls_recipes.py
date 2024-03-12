from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views_recipes

urlpatterns = [
    path('recipe/add/', views_recipes.RecipeAddView.as_view(), name='recipe_add'),
    path('recipe/add/ingredients/<int:recipe_id>/', views_recipes.RecipeAddIngredientsView.as_view(),
         name='ingredients_add'),
    path('recipes/', views_recipes.RecipesView.as_view(), name='recipes'),
    path('recipe/<int:pk>/', views_recipes.RecipeView.as_view(), name='recipe'),
    path('recipe/update/<int:pk>/', views_recipes.RecipeUpdateView.as_view(), name='recipe_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
