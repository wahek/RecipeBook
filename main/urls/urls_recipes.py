from django.urls import path

from main import views_recipes

urlpatterns = [
    path('recipe/add/', views_recipes.RecipeAddView.as_view(), name='recipe_add'),
    path('recipe/add/ingredients/<int:recipe_id>/', views_recipes.RecipeAddIngredientsView.as_view(),
         name='ingredients_add'),
    path('recipes/', views_recipes.RecipesView.as_view(), name='recipes'),
    path('recipes_category/<int:category_pk>/', views_recipes.RecipeByCategoryView.as_view(),
         name='recipes_by_category'),
    path('recipe/<int:pk>/', views_recipes.RecipeView.as_view(), name='recipe'),
    path('recipe/update/<int:pk>/', views_recipes.RecipeUpdateView.as_view(), name='recipe_update'),
    path('categories/', views_recipes.CategoriesView.as_view(), name='categories'),
    path('recipe/delete/<int:pk>/', views_recipes.RecipeDeleteView.as_view(), name='recipe_del'),
    path('recipe/restore/<int:pk>/', views_recipes.RecipeRestoreView.as_view(), name='recipe_res'),
]
