from fastapi import Depends
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from models import AccessToken, User, get_access_token_db

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="db",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)