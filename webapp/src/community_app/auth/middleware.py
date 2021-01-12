import logging

from bh.core_utils.bh_exception import BHException
from bh.services.factory import Factory
from bh_settings import get_settings


from community_app.auth.pipeline import extract_tokens

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from misago.users.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger("CommunityMiddleware")

# import debugpy
# debugpy.listen(("0.0.0.0", 8211))


def platgen_session_middleware(get_response):
    # One-time configuration and initialization.
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cookies_updated = False

        # Here we validate existence of an authentication entity but ONLY for non-admin users.
        # If we don't have an authentication entity, OR we don't have an access_token (e.g. it's expired)
        # we attempt to refresh the tokens with refresh_access_token
        #
        # If that fails, we log the user out and redirect to sleepio
        # If that suceeds, we update the tokens
        if settings.SESSION_COOKIE_NAME in request.COOKIES and not request.user.is_superuser:
            tokens = extract_tokens(request)
            access_token = tokens.get(ACCESS_TOKEN)
            refresh_token = tokens.get(REFRESH_TOKEN)
            authentication_service = Factory.create("UserAccountAuthentication", "1")
            authentication_entity = None
            if access_token or refresh_token:
                authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)
            if access_token is None or not authentication_entity:
                try:
                    tokens = authentication_service.refresh_access_token(refresh_token=refresh_token)
                    access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]
                    cookies_updated = True
                except BHException as e:
                    logger.debug(e)
                    logout(request)
                    request.user = AnonymousUser()
                    return redirect(get_settings("sleepio_app_url"))

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if cookies_updated:
            response.set_cookie(
                ACCESS_TOKEN,
                access_token,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None,
            )

            response.set_cookie(
                REFRESH_TOKEN,
                refresh_token,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None,
            )

        return response

    return middleware
