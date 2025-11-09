import uuid
from src.models import EntityRequest, AdditionRequest


def default_entity() -> EntityRequest:
    """Возвращает стандартный, полностью заполненный payload."""
    return EntityRequest(
        title="Новая тестовая сущность",
        verified=True,
        important_numbers=[10, 20, 30],
        addition=AdditionRequest(
            additional_info="Стандартная доп. информация", additional_number=123
        ),
    )


def updated_entity_payload() -> EntityRequest:
    """Возвращает payload с обновленными данными."""
    return EntityRequest(title="Обновленный заголовок", verified=False)


def verified_entity() -> EntityRequest:
    """Возвращает payload для сущности с verified=True и уникальным title."""
    unique_part = uuid.uuid4().hex[:8]
    return EntityRequest(title=f"Verified Entity {unique_part}", verified=True)


def unverified_entity() -> EntityRequest:
    """Возвращает payload для сущности с verified=False и уникальным title."""
    unique_part = uuid.uuid4().hex[:8]
    return EntityRequest(title=f"Unverified Entity {unique_part}", verified=False)
