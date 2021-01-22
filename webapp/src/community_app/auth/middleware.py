import logging

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout

# from django.shortcuts import redirect
from misago.users.models import AnonymousUser
from typing import Optional

from bh.core_utils.bh_exception import BHException
from bh.services.factory import Factory
from bh_settings import get_settings


logger = logging.getLogger("CommunityMiddleware")

#import debugpy
#debugpy.listen(("0.0.0.0", 8211))


def platgen_session_middleware(get_response):
    # One-time configuration and initialization.
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    def extract_tokens(request, *args, **kwargs) -> dict:
        return dict(access_token=request.COOKIES.get(ACCESS_TOKEN), refresh_token=request.COOKIES.get(REFRESH_TOKEN))

    def construct_cookie_domain_from_request_headers(request_headers: dict) -> Optional[str]:
        """Construct a domain string for the cookies from request headers (specifically the Origin header).

        Args:
            request_headers (dict): the request headers

        Returns:
            Optional[str]: the domain string
        """
        try:
            domain = ".".join(request_headers["host"].split(".")[1:])
            return "." + domain if domain else None
        except KeyError:
            return None

    def middleware(request, *args, **kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cookies_updated = False
        authentication_entity = None

        # Here we validate existence of an authentication entity but ONLY for non-admin users.
        # We must support admin users logging in with email, and not using Sleepio auth cookies.
        # If we don't have an authentication entity, OR we don't have an access_token (e.g. it's expired)
        # we attempt to refresh the tokens with refresh_token
        #
        # If that fails, we log the user out and redirect to sleepio
        # If that suceeds, we update the tokens
        #
        # It's important that this is placed after Misago's user middleware items, to ensure we have a
        # user attached to the session, which allows us to log the user off prior to redirecting.
        #
        # This is to avoid managing sessions directly, and using built-in behavior to log a user out.
        # If we have an authentication entity, we enrich the request to include the platform_user_id, which is used in
        # the social_auth_pipeline, fetch_user_account

        if not request.user.is_superuser:
            tokens = extract_tokens(request)
            access_token, refresh_token = tokens.get(ACCESS_TOKEN), tokens.get(REFRESH_TOKEN)
            authentication_service = Factory.create("UserAccountAuthentication", "1")
            if access_token or refresh_token:
                # TODO question, this works with either token. If we don't have a refresh token, this means we'll be redirected
                # when it times out. Problem?
                authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)
            if access_token is None or not authentication_entity:
                try:
                    tokens = authentication_service.refresh_access_token(refresh_token=refresh_token)
                    access_token, refresh_token = tokens.get(ACCESS_TOKEN), tokens.get(REFRESH_TOKEN)
                    authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)
                    cookies_updated = True
                except BHException as e:
                    logger.info(e)
                    if settings.SESSION_COOKIE_NAME in request.COOKIES:
                        logout(request)
                        request.user = AnonymousUser()
                    # TODO enable this when we have sleepio redirect URLS,
                    #   and second level domain cookies working.
                    #   Until then, this will always fire upon landing on the page
                    #   because we won't have the cookies generated
                    # return redirect(get_settings("sleepio_app_url"))

        if authentication_entity:
            request._platform_user_id = authentication_entity.get("user_id")
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if cookies_updated:
            clear_cookie_dt = datetime(year=1970, month=1, day=1)
            domain = construct_cookie_domain_from_request_headers(request.headers)
            response.set_cookie(
                ACCESS_TOKEN,
                access_token,
                expires=(datetime.utcnow() + timedelta(seconds=get_settings("access_token_cookie_expiration_seconds")))
                if access_token
                else clear_cookie_dt,
                domain=domain,
                secure=get_settings("secure_cookies", True),
                httponly=True,
            )

            response.set_cookie(
                REFRESH_TOKEN,
                refresh_token,
                expires=(datetime.utcnow() + timedelta(days=get_settings("refresh_token_cookie_expiration_days")))
                if refresh_token
                else clear_cookie_dt,
                secure=get_settings("secure_cookies", True),
                domain=domain,
                httponly=True,
            )

        return response

    return middleware
