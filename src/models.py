from typing import List, Optional
from pydantic import BaseModel, Field


class AdditionRequest(BaseModel):
    """Модель dto.AdditionRequest."""

    additional_info: Optional[str] = "Дополнительные сведения"
    additional_number: Optional[int] = 123


class AdditionResponse(BaseModel):
    """Модель dto.AdditionResponse."""

    id: int
    additional_info: str
    additional_number: int


class EntityRequest(BaseModel):
    """Модель dto.EntityRequest."""

    title: str = "Заголовок сущности по умолчанию"
    verified: bool = True

    important_numbers: List[int] = Field(default_factory=list)

    addition: AdditionRequest = Field(default_factory=AdditionRequest)


class EntityResponse(BaseModel):
    """Модель dto.EntityResponse."""

    id: int
    title: str
    verified: bool
    important_numbers: List[int] = Field(default_factory=list)
    addition: AdditionResponse


class EntityListResponse(BaseModel):
    """
    Модель для ответа от эндпоинта /getAll,
    который возвращает словарь с ключом 'entity'.
    """

    entity: List[EntityResponse]
