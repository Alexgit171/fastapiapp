from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse

from models import CalculationBody, Feedback, User, UserAge


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
STUDENT_NAME = "Ладинский Александр Владимирович"

api = FastAPI(
    title="Контрольная работа №1 - FastAPI",
    version="1.0.0",
    description=(
        "Объединённое приложение по заданиям 1.1-2.2. "
        "Корневой маршрут / возвращает HTML в браузере и JSON для API-клиентов."
    ),
)

student = User(name=STUDENT_NAME, id=1)
feedbacks: list[Feedback] = []


def _normalize_number(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


@api.get("/")
async def root(request: Request):
    """
    В одном проекте нужно закрыть сразу два задания:
    - 1.1: JSON на '/'
    - 1.2: HTML на '/'

    Поэтому для браузера отдаём HTML, а для API-клиентов - JSON.
    """

    accept_header = (request.headers.get("accept") or "").lower()
    user_agent = (request.headers.get("user-agent") or "").lower()

    wants_html = "text/html" in accept_header or "mozilla" in user_agent

    if wants_html:
        return FileResponse(INDEX_FILE)

    return {"message": "Добро пожаловать в моё приложение FastAPI!"}


@api.post("/calculate")
async def calculate(
    payload: Optional[CalculationBody] = Body(default=None),
    num1: Optional[float] = Query(default=None),
    num2: Optional[float] = Query(default=None),
):
    """
    Принимает числа либо как query-параметры, либо как JSON.
    Это делает маршрут удобным для разных способов проверки.
    """

    first = num1 if num1 is not None else (payload.num1 if payload else None)
    second = num2 if num2 is not None else (payload.num2 if payload else None)

    if first is None or second is None:
        raise HTTPException(
            status_code=422,
            detail="Передайте num1 и num2 как query-параметры или JSON-тело.",
        )

    result = _normalize_number(first + second)
    return {"result": result}


@api.get("/users")
async def get_user():
    return student.model_dump()


@api.post("/user")
async def check_user_age(user: UserAge):
    data = user.model_dump()
    data["is_adult"] = user.age >= 18
    return data


@api.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}
