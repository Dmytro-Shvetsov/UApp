from django.contrib import admin
from django.urls import path, include
from map.views import index
from map import views

urlpatterns = [
    path('', index, name="Home"),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    path('create/', views.MarkerCreateView.as_view(), name='create-marker'),
]

