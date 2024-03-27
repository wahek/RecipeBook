from django.urls import path, include

from main import views_users

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('registration/', views_users.Registration.as_view(), name='registration'),
    path('profile/', views_users.Profile.as_view(), name='profile'),
    path('profile/<int:user_id>/', views_users.ProfileByID.as_view(), name='profileID'),
    path('profile/change/', views_users.ProfileChange.as_view(), name='change_profile'),
]
