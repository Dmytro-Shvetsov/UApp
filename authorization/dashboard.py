from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def dashboard_view(request):
    if request.method == "GET":
        # Set session for the main left side bar active menu
        request.session['active_sidebar_menu'] = "dashboard"

        return render(request, 'authorization/dashboard/index.html',
                      {
                          'title': 'Dashboard',
                          'meta_desc': 'Welcome to your dashboard',
                          'active_sidebar_menu': request.session['active_sidebar_menu']
                       })