from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('security/', views.security_view, name='security_page'),
    path('profile/', views.profile_view, name='profile_page')
]
