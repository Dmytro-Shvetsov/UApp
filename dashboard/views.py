from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authorization.forms import ChangePasswordForm
from authorization import functions as f
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from authorization.forms import UpdateUserProfileForm
from authorization.functions import dict_alert_msg
import os

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


@login_required
def profile_view(request):
    user_profile = request.user.profile
    if request.method == "GET":
        update_profile_form = UpdateUserProfileForm(initial={
            "first_name": user_profile.first_name or '',
            "last_name": user_profile.last_name or '',
            "bio": user_profile.bio or '',
            "company": user_profile.company or "",
            "current_position": user_profile.current_position or "",
            "user_email_is_public": request.user.profile.user_email_is_public
        })
        context = {
            'update_profile_form': update_profile_form
        }
        return render(request, 'dashboard/profile.html', context)

    response = dict()
    if request.method == "POST":
        update_profile_form = UpdateUserProfileForm(request.POST, request.FILES)
        if update_profile_form.is_valid():
            profile_data = {}
            f_name = update_profile_form.cleaned_data['first_name']
            user_profile.first_name = f_name if f_name is not None else ''

            l_name = update_profile_form.cleaned_data['last_name']
            user_profile.last_name = l_name if f_name is not None else ''

            bio = update_profile_form.cleaned_data['bio']
            user_profile.bio = bio if bio is not None else ''

            company = update_profile_form.cleaned_data['company']
            user_profile.company = company if company is not None else ''

            current_position = update_profile_form.cleaned_data['current_position']
            user_profile.current_position = current_position if current_position is not None else ''

            user_profile.user_email_is_public = True if 'user_email_is_public' in request.POST else False

            image = update_profile_form.cleaned_data['image']
            if image is not None and image.name != settings.DEFAULT_AVATAR:
                if user_profile.image.name != settings.DEFAULT_AVATAR:
                    os.remove(os.path.join(settings.MEDIA_ROOT, user_profile.image.name))
                user_profile.image = image

            user_profile.save()

            msg = 'Ви успішно оновили ваш профіль.'
            response = dict_alert_msg('True', 'Оновлення профілю', msg)

        else:
            response = dict_alert_msg('False', 'Оновлення профілю', 'Щось пішло не так', update_profile_form.errors)

    return JsonResponse(response)


@login_required
def dashboard_view(request):
    context = {
        'page': request.GET.get('page') if request.GET.get('page') is not None else 'profile'
    }
    return render(request, 'dashboard/index.html', context)
