import logging

from django.shortcuts import redirect

from bh.services.factory import Factory
from misago.socialauth.pipeline import perpare_username

from .exceptions import MissingOptionalParameters, UserNotAuthenticated, ExpiredRefreshToken, InvalidTokens


logger = logging.getLogger("CommunityPipeline")


def extract_tokens(request, *args, **kwargs) -> dict:
    return dict(access_token=request.COOKIES.get("access_token"), refresh_token=request.COOKIES.get("refresh_token"))


def validate_tokens(access_token: str, refresh_token: str, *args, **kwargs) -> dict:
    community_app_service = Factory.create("CommunityApp", "1")
    try:
        authentication_entity = community_app_service.validate_tokens(access_token=access_token, refresh_token=refresh_token)
        if not authentication_entity:
            raise InvalidTokens
    except (MissingOptionalParameters, UserNotAuthenticated, ExpiredRefreshToken, InvalidTokens):
        logger.debug("Error in validating tokens. Redirecting to Sleepio...")
        return redirect("/login/sleepio")  # TODO Add query string to redirect back to Community

    return dict(
        access_token=authentication_entity.get("access_token"),
        refresh_token=authentication_entity.get("refresh_token"),
        user_id=authentication_entity.get("user_id"),
    )


def fetch_user_account(user_id: int, *args, **kwargs) -> dict:
    user_account_entity = Factory.create("UserAccount", "1").read(entity_id=user_id)
    return dict(user_account=user_account_entity)


def get_username(details, *args, **kwargs) -> dict:
    return {"clean_username": perpare_username(details["username"])}


def social_details(backend, user_account, details, *args, **kwargs):
    return {'details': dict(backend.get_user_details(user_account), **details)}
