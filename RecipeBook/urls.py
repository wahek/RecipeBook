from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from main.urls import urls_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls_index)),
    path('auth/', include('main.urls.urls_users')),
    path('book/', include('main.urls.urls_recipes')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)