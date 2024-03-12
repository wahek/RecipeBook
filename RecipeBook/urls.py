from django.contrib import admin
from django.urls import path, include
from main.urls import urls_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls_index)),
    path('auth/', include('main.urls.urls_users')),
    path('book/', include('main.urls.urls_recipes')),
]
