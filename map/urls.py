from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='map'),
    path('admin/', admin.site.urls),
    path('create/', views.MarkerCreateView.as_view(), name='create-marker'),
    path('marker_info/', views.marker_info_view, name='marker_info'),
    path('estimate_marker/', views.estimate_marker_view, name='estimation'),
    path('follow/', views.follow_view, name='follow')
]
