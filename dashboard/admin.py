from django.contrib import admin
from authorization.models import UserProfile

admin.site.site_header = 'Uapp admin panel'
admin.site.register(UserProfile)
