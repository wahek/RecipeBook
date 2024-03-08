from django.urls import path, include

from . import views_users

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('registration/', views_users.Registration.as_view(), name='registration'),
]