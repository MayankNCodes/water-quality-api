from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Water Quality Analysis API',
        'version': '1.0.0',
        'endpoints': {
            'samples': '/api/water-quality/samples/',
            'create_and_report': '/api/water-quality/create-and-report/',
            'admin': '/admin/',
            'docs': 'https://github.com/yourusername/water-quality-api'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/water-quality/', include('water_quality.urls')),
    path('', api_root, name='api_root'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
