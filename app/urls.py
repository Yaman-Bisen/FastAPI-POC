from fastapi import APIRouter
from app.controllers.users import index, UserAPI

app_router = APIRouter()

app_router.add_api_route("/", index, methods=["GET"], response_model=list)
app_router.add_api_route("/create_user", UserAPI().create_user, methods=["POST"], dependencies=[])
app_router.add_api_route("/delete_user", UserAPI().delete_user, methods=["POST"], dependencies=[])
