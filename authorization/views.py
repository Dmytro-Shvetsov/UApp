from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SignUpForm, LoginAuthenticationForm, PasswordResetForm, PasswordResetConfirmForm
from . import functions as f
from uapp import settings as config
from django.core.mail import send_mail
from .tokens import account_activation_token, default_token_generator
import requests


def register_view(request):

    if request.method == 'GET':
        form = SignUpForm()
        context = {
            'form': form,
            'GRECAP_SITE_KEY': config.GRECAP_SITE_KEY
        }
        return render(request, 'authorization/registration/registration.html', context)

    response = dict()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        is_pass_valid, error_msg, error_title1 = f.is_password_valid(password1, password2)
        is_user_name_valid, error_msg2, error_title2 = f.is_username_valid(username)

        if not is_user_name_valid:
            response = f.dict_alert_msg('False', error_title1, error_msg)

        elif not is_pass_valid:
            response = f.dict_alert_msg('False', error_title1, error_msg)

        elif User.objects.filter(email=email):
            # Check if email exist in our users list
            error_title = 'Invalid Email!'
            error_msg = """A user with that email address already exist."""
            response = f.dict_alert_msg('False', error_title, error_msg)

        elif User.objects.filter(username=username):
            error_title = 'Invalid Username!'
            error_msg = """Username already taken, please try another one."""
            response = f.dict_alert_msg('False', error_title, error_msg)
        else:
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            response = {
                'secret': config.GRECAP_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(config.GRECAP_VERIFY_URL, data=response)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                # Validate email address if exist from an email server.
                is_email_real = f.is_email_valid(email)

                if is_email_real:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)

                    subject = 'Activate Your ' + \
                              str(config.SITE_SHORT_NAME) + ' Account'
                    activation_page_context = {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        }
                    message = render_to_string(
                        'authorization/registration/account_activation_email.html',
                        activation_page_context
                        )
                    to_list = [email, config.EMAIL_HOST_USER]
                    send_mail(subject, message, config.EMAIL_HOST_USER, to_list, fail_silently=False)

                    error_title = 'Awesome'
                    error_msg = """New user has been created successfully!"""
                    response = f.dict_alert_msg('True', error_title, error_msg,)
                else:
                    error_title = 'Oops, Invalid Email Address'
                    error_msg = """Invalid or non-existed email address."""
                    response = f.dict_alert_msg('False', error_title, error_msg)

            else:
                error_msg = """Invalid reCAPTCHA, please try again."""
                response = f.dict_alert_msg('False', 'Oops, Error', error_msg, 'error')

        # Return some json response back to user
        return JsonResponse(response)


def account_activation_sent(request):
    return render(request, 'authorization/registration/account_activation_sent.html',
                  {'title': 'New ' + str(config.SITE_SHORT_NAME) +
                            ' Account Activation',
                   'meta_desc': 'New account activation.'})


def activate(request, uidb64, token):
    """ Function to call for new user account activation process."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return render(request,
                      'authorization/registration/account_activation_complete.html',
                      {
                          'title': 'New Account Activated Successfully',
                          'meta_desc': 'New Account Activated Successfully'
                      }
                      )
    else:
        return render(request,
                      'authorization/registration/account_activation_fail.html',
                      {
                          'title': 'Account Activation Failed',
                          'meta_desc': 'Account Activation Failed'
                      }
                      )


def login_view(request):
    if request.user.is_authenticated:
        # User has been Authenticated: redirect to the specified landing page instead
        return redirect(config.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'GET':
            # Get login form to display
            form = LoginAuthenticationForm()
            return render(request, 'authorization/login.html',
                          {'form': form,
                           'title': 'Log in',
                           'meta_desc': config.SITE_SHORT_NAME + """ Account.
                           Sign in to access your account.""",
                           'GRECAP_SITE_KEY': config.GRECAP_SITE_KEY
                           },
                          )

        response = dict()
        if request.method == 'POST':
            form = LoginAuthenticationForm(request.POST)
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            chkKeepMe = request.POST.get('chkKeepMe')

            if username and password:

                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                response = {
                    'secret': config.GRECAP_SECRET_KEY,
                    'response': recaptcha_response
                }
                r = requests.post(config.GRECAP_VERIFY_URL, data=response)
                result = r.json()

                ''' End reCAPTCHA validation '''
                if result['success']:
                    # Check remember me checkbox option
                    if chkKeepMe == "on":
                        request.session.set_expiry(2592000)  # 30 days
                    else:
                        # session will expire on 12 hrs
                        request.session.set_expiry(43200)

                    # Test username/password combination
                    user = authenticate(username=username, password=password)

                    if user is not None:
                        # User is active
                        if user.is_active:
                            # Login Successfully Authenticated
                            login(request, user)

                            alert_title = 'Login Successfully'
                            alert_message = """User has been successfully login."""
                            response = f.dict_alert_msg('True', alert_title,
                                                  alert_message)

                            response["BASE_URL"] = config.BASE_URL

                            # Check /next/ url parameter
                            next_url = request.GET.get('next')
                            if next_url:
                                # Strip off "/" at the first string position
                                response["redirect_url"] = next_url[1:]
                            else:
                                response["redirect_url"] = config.LOGIN_REDIRECT_URL

                        else:
                            # Account is not Active
                            alert_title = 'Account is not Active'
                            alert_message = """Sorry, your account is not active, please
                            check your email inbox to verify your account."""
                            response = f.dict_alert_msg('False', alert_title,
                                                  alert_message)
                    else:
                        # Invalid username or password
                        alert_title = 'Invalid Login'
                        alert_message = """Please enter the correct username and password for your account.
                        Note that both fields may be case-sensitive."""
                        response = f.dict_alert_msg('False', alert_title, alert_message)
                else:
                    alert_title = 'Oops, Error'
                    alert_message = """Invalid reCAPTCHA, please try again."""
                    response = f.dict_alert_msg('False', alert_title, alert_message)

    return JsonResponse(response)


def password_reset_view(request):
    """Renders the password reset page."""
    if request.method == 'GET':
        # Get password reset form to display
        form = PasswordResetForm()
        return render(request, 'authorization/account/password_reset_form.html',
                      {'form': form, 'title': 'Reset Password',
                       'meta_desc': """We can help you to reset your password using your
                       registered email linked to your account.""",
                       'GRECAP_SITE_KEY': config.GRECAP_SITE_KEY})

    response = dict()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            response = {
                'secret': config.GRECAP_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(config.GRECAP_VERIFY_URL, data=response)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                # Check first if email existed in our users data
                if User.objects.filter(email=form.cleaned_data.get("email")):
                    # Setup email template
                    opts = {
                        'use_https': request.is_secure(),
                        'token_generator': default_token_generator,
                        'from_email': config.APP_EMAIL_FROM,
                        'email_template_name': 'authorization/account/password_reset_email.html',
                        'subject_template_name': 'authorization/account/password_reset_subject.txt',
                        'request': request
                    }
                    form.save(**opts)

                    msg = """Password reset request sent successfully."""
                    response = f.dict_alert_msg('True', 'Password Reset Sent!', msg)
                    response["redirect_url"] = '/auth/password_reset/done/'
                    response["base_url"] = config.BASE_URL

                else:
                    # Email submitted is not found in our users data
                    msg = """Email is not registered, please try again."""
                    response = f.dict_alert_msg('False', 'Email is Not Registered!', msg)
            else:
                msg = """Invalid reCAPTCHA, please try again."""
                response = f.dict_alert_msg('False', 'Oops, Error', msg)

        else:
            error_title = 'Validation error'
            error_msg = 'Form did not validate'
            response = f.dict_alert_msg('False', error_title, error_msg, form.errors)
            response['form_errors'] = form.errors

        return JsonResponse(response)


def password_reset_confirm_view(request, uidb64, token):
    if request.method == 'GET':
        # Get user info
        current_user = request.user
        formChangePassword = PasswordResetConfirmForm(current_user.username)

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            validlink = True
        else:
            validlink = False

        return render(request, 'authorization/account/password_reset_confirm.html',
                      {
                          'title': 'Password Reset Confirm',
                          'meta_desc': 'Password Reset Confirm.',
                          'formChangePassword': formChangePassword,
                          'validlink': validlink,
                          'username': user,
                          'GRECAP_SITE_KEY': config.GRECAP_SITE_KEY
                      })


def password_reset_done_view(request):
    if request.method == 'GET':
        # Get password reset done page to display
        return render(request, 'authorization/account/password_reset_done.html',
                      {'title': 'Password Reset Sent',
                       'meta_desc': """We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.
                       If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder."""})


def submit_new_password_view(request):
    response = dict()
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        username = request.POST.get('username')

        is_pass_valid, msg, title = f.is_password_valid(new_password1, new_password2)

        if not is_pass_valid:
            response = f.dict_alert_msg('False', title, msg)
        else:
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            response = {
                'secret': config.GRECAP_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(config.GRECAP_VERIFY_URL, data=response)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                # Check first if email existed in our users data
                if User.objects.filter(username=username):
                    # Change the password now
                    u = User.objects.get(username=username)
                    u.set_password(new_password1)
                    u.save()

                    msg = """Your new password was successfully changed."""
                    response = f.dict_alert_msg('True', 'Password Changed', msg)
                else:

                    # The username submitted is not found in our users data
                    msg = """Oops, username not found, please try again."""
                    response = f.dict_alert_msg('False', 'Username Not Found!', msg)
            else:
                msg = """Invalid reCAPTCHA, please try again."""
                response = f.dict_alert_msg('False', 'Oops, Error', msg)

        return JsonResponse(response)


def password_reset_complete_view(request):
    if request.method == 'GET':
        # Get password reset done page to display
        return render(request, 'authorization/account/password_reset_complete.html',
                      {'title': 'Password Reset Complete',
                       'meta_desc': """Your password has been set, you can login with your account with us now."""})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        # Redirect to a success page.
        return redirect('/auth/login/')
