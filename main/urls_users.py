from django.urls import path

from . import views_users

urlpatterns = [
    path('user/', views_users.index, name='index'),
    path('signin/', views_users.signin, name='signin'),
    path('registration/', views_users.registration, name='registration'),
]
