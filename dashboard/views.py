from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authorization.forms import ChangePasswordForm
from authorization import functions as f
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate


@login_required
def security_view(request):
    if request.method == "GET":
        current_user = request.user
        formChangePassword = ChangePasswordForm(current_user.username)

        return render(request, 'dashboard/security.html',
                      {
                          'title': 'Change Password',
                          'meta_desc': 'Change your password.',
                          'formChangePassword': formChangePassword,
                       })

    response = dict()
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Get user info
        current_user = request.user

        is_pass_valid, msg, title = f.is_password_valid(new_password1, new_password2)

        if not is_pass_valid:
            response = f.dict_alert_msg('False', title, msg, 'error')
        else:
            user = authenticate(username=current_user.username, password=old_password)
            if user is not None:
                if User.objects.filter(username=current_user.username):
                    # Change the password now
                    u = User.objects.get(username=current_user.username)
                    u.set_password(new_password1)
                    u.save()

                    msg = """Your new password was successfully changed."""
                    response = f.dict_alert_msg('True', 'Password Changed', msg)
                else:
                    # The username submitted is not found in our users data
                    msg = """Oops, username not found, please try again."""
                    response = f.dict_alert_msg('False', 'Username Not Found!', msg)
            else:
                msg = """Re-enter your old password!"""

                response = f.dict_alert_msg('False', 'Old password is not valid.', msg)

        return JsonResponse(response)


def profile_view(request):
    if request.method == "GET":
        return render(request, 'dashboard/profile.html')


@login_required
def dashboard_view(request):
    page = request.GET.get('page') if request.POST.get('page') is None else request.POST.get('page')
    if page is None:
        return render(request, 'dashboard/index.html')
    else:
        if page.upper() == 'SECURITY':
            return security_view(request)





