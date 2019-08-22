from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.shortcuts import render
import requests
from .forms import SignUpForm


# def register_view(request):
#
#     if request.method == 'GET':
#         form = SignUpForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'authorization/register_form.html', context)
#
#     response = dict()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#
#         is_pass_valid, error_msg, error_title1 = is_password_valid(password1, password2)
#         is_user_name_valid, error_msg2, error_title2 = is_username_valid(username)
#
#         if not is_user_name_valid:
#             # Return some json response back to user
#             data = dict_alert_msg('False', title1, msg1, 'error')
#
#         elif not is_pass_valid:
#             # Return some json response back to user
#             data = dict_alert_msg('False', title, msg, 'error')
#
#             # Check if email exist in our users list
#         elif User.objects.filter(email=email):
#             # Return some json response back to user
#             msg = """A user with that email address already exist."""
#             data = dict_alert_msg('False', 'Invalid Email!', msg, 'error')
#
#         elif User.objects.filter(username=username):
#             # Return some json response back to user
#             msg = """Username already taken, please try another one."""
#             data = dict_alert_msg('False', 'Invalid Username!',
#                                   msg, 'error')
#
#             # To check prohibited username match with our list
#         elif SiteConfig.objects.filter(property_name=username):
#             # Return some json response back to user
#             msg = """A username you have entered is not allowed."""
#             data = dict_alert_msg('False', 'Prohibited Username!',
#                                   msg, 'error')
#
#             # To check if Prohibited email match with our list
#         elif SiteConfig.objects.filter(property_name=email):
#             # Return some json response back to user
#             msg = """The email you have entered is not allowed."""
#             data = dict_alert_msg('False', 'Prohibited Email!',
#                                   msg, 'error')
#
#         else:
#
#             ''' Begin reCAPTCHA validation '''
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             data = {
#                 'secret': settings.GRECAP_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             r = requests.post(settings.GRECAP_VERIFY_URL, data=data)
#             result = r.json()
#             ''' End reCAPTCHA validation '''
#
#             if result['success']:
#
#                 # Validate email address if exist from an email server.
#                 is_email_real = is_email_valid(email)
#
#                 if is_email_real:
#
#                     # Proceed with the rest of registering new user
#                     user = form.save(commit=False)
#                     user.is_active = False
#                     user.save()  # Finally save the form data
#                     user.pk  # Get the latest id
#
#                     current_site = get_current_site(request)
#                     subject = 'Activate Your ' + \
#                               str(settings.SITE_SHORT_NAME) + ' Account'
#                     message = render_to_string(
#                         'myroot/account/account_activation_email.html',
#                         {
#                             'user': user,
#                             'domain': current_site.domain,
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#                             'token': account_activation_token.make_token(user),
#                         })
#                     user.email_user(subject, message, settings.APP_EMAIL_FROM)
#
#                     # Return some json response back to user
#                     msg = """New user has been created successfully!"""
#                     data = dict_alert_msg('True', 'Awesome', msg, 'success')
#
#                 else:
#
#                     # Return some json response back to user
#                     msg = """Invalid or non-existed email address."""
#                     data = dict_alert_msg('False', 'Oops, Invalid Email Address', msg, 'error')
#
#             else:
#
#                 # Return some json response back to user
#                 msg = """Invalid reCAPTCHA, please try again."""
#                 data = dict_alert_msg('False', 'Oops, Error', msg, 'error')
#
#         return JsonResponse(data)
#





def login(request):
    context = {}
    if request.is_ajax() is False:
        context['template_path'] = 'base.html'
    else:
        context['template_path'] = 'authorization/base.html'
    return render(request, 'authorization/templates/registration/login.html', context)

