from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import re


def is_email_valid(email):
    try:
        validate_email(email)
    except ValidationError:
        return False

    return True


def is_password_valid(password1, password2):
    is_pass_valid = False
    error_msg, error_title = '', ''

    if password1 != password2:
        error_msg = "Passwords do not match, please try again."
        error_title = 'Password Not Match'

    elif len(password1) < settings.MIN_PASS_LENGTH:
        error_title = 'Password Too Short'
        error_msg = 'Make your password longer'

    elif not re.findall('\d', password1):
        error_msg = "The password must contain at least 1 digit from 0-9."
        error_title = 'Password No Number'

    elif not re.findall('[A-Z]', password1):
        error_msg = "The password must contain at least 1 uppercase letter from A-Z."
        error_title = 'Password No Upper'

    elif not re.findall('[a-z]', password1):
        error_msg = "The password must contain at least 1 lowercase letter from a-z."
        error_title = 'Password No Lower'

    else:
        is_pass_valid = True

    return is_pass_valid, error_msg, error_title


def is_username_valid(username):
    is_user_name_valid = False
    error_msg, error_title = '', ''

    if not re.findall(r'^[\w.@+-]+\Z', username):
        # Display error message, only allow special characters @, ., +, -, and _.
        msg = "Enter a valid username. This value may contain only alphanumeric values and @/./+/-/_ characters."
        title = 'Invalid Username'
    else:
        is_user_name_valid = True

    return is_user_name_valid, error_msg, error_title


def dict_alert_msg(is_success, title, msg, form_errors=None):
    result = {
        'alert_type': 'success' if is_success == 'True' else 'fail',
        'alert_title': title,
        'alert_message': msg,
        'form_errors': form_errors
    }
    return result
