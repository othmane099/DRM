import os
import sys

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

sys.path.append(f"{os.getcwd()}/src")
from auth.api import auth_router
from categories.api import categories_router
from containers import Container
from documents.api import documents_router
from tags.api import tags_router
from users.api import users_router

Container()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(categories_router)
api_router.include_router(tags_router)
api_router.include_router(documents_router)
app.include_router(api_router)
