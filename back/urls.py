from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
