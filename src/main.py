from fastapi import FastAPI, Depends, HTTPException, APIRouter,  Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from auth.base_configs import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operations
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from chat.router import router as router_chat
from configs import REDIS_HOST, REDIS_PORT

app = FastAPI(
    title='Trading App'
)

# Додамо дерикторію з статичними файлами
app.mount("/static", StaticFiles(directory="../static"), name="static")

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

app.include_router(router_operations)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)

# Перевірка дозволів для доступу сайту
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
        "DELETE",
        "PATCH",
        "PUT"
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        'Access-Control-Allow-*',
        "Authorization"
    ],
)

# Перевірка redis для cache
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# yield
async def get_async_session():
    print("Получение сессии")
    session = "session"
    yield session
    print("Уничтожение сессии")


@app.get("/items")
async def get_items(session=Depends(get_async_session)):
    print(session)
    return [{"id": 1}]


# parameters
def pagination_params(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}


@app.get("/subjects")
async def get_subjects(pagination_params: dict = Depends(pagination_params)):
    return pagination_params


# class
class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


@app.get("/subjects_class")
async def get_subjects_class(pagination_params: Paginator = Depends()):
    return pagination_params


# dependencies = [Depends(...)]
# class call
# request

class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Запрещено")
        # Перевірка в куках чи права доступу ций користувач
        return True


auth_guard_payments = AuthGuard("payments")


router = APIRouter(
    dependencies=[Depends(auth_guard_payments)]
)


@app.get("/payments")
def get_payments():
    return "my payments...."


# Інший метод для  middleware
# @app.middleware("http")
# async def home(request: Request):
#     return 1

# Приклад cache 1
# @cache()
# async def get_cache():
#     return 1

# Приклад cache 2
# @app.get("/cache")
# @cache(expire=60)
# async def index():
#     return dict(hello="world")


# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.email}"

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# users = [
#     {'id': 1, 'role': 'admin', 'name': 'Mario'},
#     {'id': 2, 'role': 'investor', 'name': 'Luigi'},
#     {'id': 3, 'role': 'trader', 'name': 'Bob', 'degree': [
#         {'id': 1, 'created_at': '2024-01-01T00:00:00', 'type_degree': 'expert'}
#     ]},
# ]
#
#
# class DegreeType(Enum):
#     expert = 'expert'
#     newbie = 'newbie'
#
#
# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: DegreeType
#
#
# class User(BaseModel):
#     id: int
#     role: str
#     name: str
#     degree: List[Degree] = None  # Successful Response better than down
#     # degree: Optional[List[Degree]] = []
#
#
# @app.get("/users/{user_id}", response_model=List[User])
# async def get_user(user_id: int) -> list[dict]:
#     return [user for user in users if user.get('id') == user_id]
#
#
# @app.put("/users/{user_id}")
# async def update_user(user_id: int, name: str, role: str) -> dict:
#     current_user = list(filter(lambda user: user.get('id') == user_id, users))[0]
#     current_user['name'] = name
#     current_user['role'] = role
#     return {'status': 200, 'data': current_user}
#
#
# fake_trades = [
#     {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
#     {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
# ]
#
#
# @app.get("/trades")
# async def get_trades(limit: int = 1, offset: int = 0) -> list[dict]:
#     return fake_trades[offset:][:limit]  # offset шаг limit количество
#
#
# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=10)
#     side: str
#     price: float = Field(ge=0)  # price > 0
#     amount: float
#
#
# @app.post("/trades")
# async def add_trades(trades: List[Trade]):
#     fake_trades.extend(trades)
#     return {'status': 200, 'data': fake_trades}
