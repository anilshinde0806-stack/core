# dashboard/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ✅ Include your app's urls
    path('api/', include('api.urls')),  # ߑ New API route
    path('cart1/', include('cart1.urls')),  # ߑ New API route
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

