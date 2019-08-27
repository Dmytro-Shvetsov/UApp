from django.contrib import admin
from django.urls import path, include
from . import views
from . import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('register/account_activation_sent/', views.account_activation_sent),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate,
         name='activate'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset/submit_new_password/', views.submit_new_password_view, name='submit_new_password'),
    path('password_reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', dashboard.dashboard_view, name='dashboard')
]
