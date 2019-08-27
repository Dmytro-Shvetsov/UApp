from django.contrib import admin
from django.urls import path, include
from map.views import index


urlpatterns = [
    path('', index, name="Home"),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    path('auth/', include('authorization.urls'))
]
