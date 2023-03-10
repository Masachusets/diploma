import uvicorn

from fastapi import FastAPI, Depends
from auth.base_config import fastapi_users, auth_backend, current_active_user
from auth.schemas import UserRead, UserCreate
from ordering_goods.router import router_shop, router_category
from src.db.models import User

app = FastAPI(title="Ordering goods by FastAPI")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"


app.include_router(router_shop)
app.include_router(router_category)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
