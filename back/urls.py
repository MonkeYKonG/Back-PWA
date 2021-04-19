from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

admin.autodiscover()

urlpatterns = [
  path('admin/', admin.site.urls),
  path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
  path('', include('api.urls')),
  path('doc/', TemplateView.as_view(
      template_name='redoc.html',
      extra_context={'schema_url': 'openapi-schema'}
  ), name='redoc'),
  path('openapi/', get_schema_view(
      title="PWA",
      description="PWA project",
      version="1.0.0",
      authentication_classes=[],
      permission_classes=[],
      public=True
  ), name='openapi-schema')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
