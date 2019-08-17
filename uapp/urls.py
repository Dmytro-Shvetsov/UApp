from django.contrib import admin
from django.urls import path, include
from .views import MainView

urlpatterns = [
    path('', MainView.as_view(), name="Home"),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls'))
]
