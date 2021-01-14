from bh.entities import SQLEntity
from bh.services.base_service import BaseService
from bh.services.factory import Factory


class CommunityApp(BaseService):
    """
    This is a community-app-web only service.
    It will not be published anywhere and will not be exposed to any other service.
    It is only intended to be used as an interface between the community web app and external BH services.
    """

    def validate_tokens(self, access_token: str = None, refresh_token: str = None) -> SQLEntity:
        """Validate tokens provided. If access_token is None, attempt to refresh tokens.

        Args:
            access_token (str, optional): access token of the session. Defaults to None.
            refresh_token (str, optional): refresh token of the session. Defaults to None.

        Returns:
            SQLEntity: the UserAccountAuthentication entity
        """
        authentication_service = Factory.create("UserAccountAuthentication", "1")

        # if not access_token:
            # Access token is expired, use refresh token to get new tokens
        #    tokens = authentication_service.refresh_access_token(refresh_token=refresh_token)
        #    access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]

        return authentication_service.find_with_tokens(access_token=access_token, refresh_token=refresh_token)
