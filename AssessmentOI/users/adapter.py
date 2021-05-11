from allauth.account.adapter import app_settings as app_settings_adapter
from allauth.utils import import_attribute
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from . import app_settings
from django.shortcuts import resolve_url

def get_adapter(request=None):
    # app_settings_adapter.LOGOUT_REDIRECT_URL = app_settings.LOGOUT_REDIRECT_URL
    return import_attribute(app_settings_adapter.ADAPTER)(request)
    # return import_attribute('LogoutDefaultAccountAdapter')(request)

class UsersDefaultAccountAdapter(DefaultAccountAdapter):

    def get_logout_redirect_url(self, request):
        """
        Returns the URL to redirect to after the user logs out. Note that
        this method is also invoked if you attempt to log out while no users
        is logged in. Therefore, request.user is not guaranteed to be an
        authenticated user.
        """
        return resolve_url(app_settings.LOGOUT_REDIRECT_URL)
    pass