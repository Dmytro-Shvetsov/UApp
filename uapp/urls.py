from django.contrib import admin
from django.urls import path, include
from map.views import index
from map import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name="Home"),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    path('auth/', include('authorization.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('create/', views.MarkerCreateView.as_view(), name='create-marker'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
