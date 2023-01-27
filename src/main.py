import uvicorn

from fastapi import FastAPI
from auth.base_config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate
from ordering_goods.router import router_shop, router_category

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

app.include_router(router_shop)
app.include_router(router_category)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
