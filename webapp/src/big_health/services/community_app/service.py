from bh.entities import SQLEntity
from bh.services.base_service import BaseService
from bh.services.factory import Factory


class CommunityApp(BaseService):
    """
    This is a community-app-web only service.
    It will not be published anywhere and will not be exposed to any other service.
    It is only intended to be used as an interface between the community web app and external BH services.
    """

    def validate_tokens(self, access_token: str, refresh_token: str) -> SQLEntity:
        authentication_service = Factory.create("UserAccountAuthentication", "1")
        authentication_entity = authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)

        if not authentication_entity:
            raise Exception("Tokens not found. Redirect to Sleepio")

        if not authentication_service.is_refresh_token_valid(
            refresh_token=refresh_token,
            user_id=authentication_entity.get("user_id"),
            device_fingerprint=authentication_entity.get("device_fingerprint"),
            product_id=authentication_entity.get("product_id"),
        ):
            # This is not a great user experience.
            # We will likely need to be able to refresh tokens and set those cookies within the community app without going back to Sleepio.
            # TODO
            raise Exception("Refresh token expired. Redirect to Sleepio to do refreshing.")

        return authentication_entity
