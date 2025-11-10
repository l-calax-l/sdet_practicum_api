class ApiEndpoints:
    """Класс-контейнер для эндпоинтов."""

    CREATE_ENTITY = "/create"
    GET_ALL_ENTITIES = "/getAll"

    @staticmethod
    def get_entity_by_id(entity_id: int) -> str:
        return f"/get/{entity_id}"

    @staticmethod
    def update_entity_by_id(entity_id: int) -> str:
        return f"/patch/{entity_id}"

    @staticmethod
    def delete_entity_by_id(entity_id: int) -> str:
        return f"/delete/{entity_id}"
