from django.urls import path
from .. import views_recipes
urlpatterns = [
    path('', views_recipes.IndexView.as_view(), name='index'),
]