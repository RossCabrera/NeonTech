from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path('', views.show_start_page),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
]

# Esto solo es necesario para el entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
