from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator


FORBIDDEN_WORDS_PATTERN = re.compile(
    r"\b(?:кринж\w*|рофл\w*|вайб\w*)\b",
    re.IGNORECASE,
)


class User(BaseModel):
    """Модель для задания 1.4."""

    name: str
    id: int


class UserAge(BaseModel):
    """Модель для задания 1.5*."""

    name: str
    age: int


class CalculationBody(BaseModel):
    """Тело запроса для задания 1.3*."""

    num1: float
    num2: float


class Feedback(BaseModel):
    """Модель для заданий 2.1 и 2.2*."""

    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        if FORBIDDEN_WORDS_PATTERN.search(value):
            raise ValueError("Использование недопустимых слов")
        return value
