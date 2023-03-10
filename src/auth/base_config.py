from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend

from src.auth.manager import get_user_manager
from src.auth.utils import get_cookie_transport, get_jwt_strategy
from src.db.models import User


auth_backend = AuthenticationBackend(
    name="db",
    transport=get_cookie_transport(),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

current_active_user = fastapi_users.current_user(active=True)
