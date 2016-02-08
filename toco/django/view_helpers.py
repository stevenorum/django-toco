from django.conf import settings
import logging
from toco.django.user import *

logger = logging.getLogger(__name__)

def get_reset_code(email):
    reset_request = PasswordResetRequest(email=email)
    reset_request.create()
    return reset_request.id

def reset_password_from_code(new_password, reset_code):
    request = PasswordResetRequest(reset_code)
    user = User.load_from_password_reset_request(request)
    user.set_password(new_password)
    user.save()
    request.expire()

def reset_password(new_password, user, current_password):
    if not user.password_is_correct(current_password):
        raise RuntimeError("Password provided is incorrect.")
    user.set_password(new_password)
    user.save()

def login_from_request(request, **session_args):
    return login(email=request.POST.get('email'), password=request.POST.get('password'), HTTP_USER_AGENT=request.META.get("HTTP_USER_AGENT"), REMOTE_ADDR=request.META.get("REMOTE_ADDR"), **session_args)

def login(email, password, **session_args):
    user = None
    session = None
    cookie_args = None

    if email and password:
        user = User.load_with_auth(email, password)
        if user:
            session = user.get_new_session_token(**session_args)
            cookie_args = {'key':SessionToken.CKEY, 'value':session.id, 'expires':session.expiry_datetime, 'secure':settings.TOCO_SECURE_SESSION_COOKIES, 'httponly':True}

    return user, session, cookie_args

def logout(session=None, request=None):
    if request:
        try:
            request.session.expire()
        except AttributeError:
            pass
    if session:
        try:
            session.expire()
        except AttributeError:
            pass
    return

def logout_everywhere(user=None, request=None):
    if request:
        try:
            request.user.purge_sessions()
        except AttributeError:
            pass
    if user:
        try:
            user.purge_sessions()
        except AttributeError:
            pass
    return

def register(email, password, **session_args):
    user = None
    session = None
    cookie_args = None
    try:
        if email and password:
            user = User(email=email)
            user.set_password(password)
            user.create()
            session = user.get_new_session_token(**session_args)
            cookie_args = {'key':SessionToken.CKEY, 'value':token.id, 'expires':token.expiry_datetime, 'secure':settings.settings.TOCO_SECURE_SESSION_COOKIES, 'httponly':True}
    except:
        pass
    return user, session, cookie_args

def register_from_request(request, **session_args):
    return register(email=request.POST.get('email'), password=request.POST.get('password'), HTTP_USER_AGENT=request.META.get("HTTP_USER_AGENT"), REMOTE_ADDR=request.META.get("REMOTE_ADDR"), **session_args)
