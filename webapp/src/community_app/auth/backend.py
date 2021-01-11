import logging

from social_core.backends.base import BaseAuth

from bh_settings import get_settings


logger = logging.getLogger("SleepioAuth")


class SleepioAuth(BaseAuth):
    name = "sleepio"
    supports_inactive_user = False

    def get_user_details(self, user_account):
        return {
            "username": user_account.get("uuid")[:12],  # TODO temporary
            "email": user_account.get("email_address"),
            "fullname": f"{user_account.get('first_name')} {user_account.get('last_name')}",
            "first_name": user_account.get("first_name"),
            "last_name": user_account.get("last_name"),
        }

    def get_user_id(self, user_account, *args, **kwargs):
        return user_account.get("id")

    def auth_url(self):
        return get_settings("sleepio_app_url")

    def auth_complete(self, *args, **kwargs):
        kwargs.update({"response": self.data, "backend": self})
        return self.strategy.authenticate(*args, **kwargs)
