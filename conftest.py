import pytest
import os
from dotenv import load_dotenv
from src.api_client import ApiClient
from src.models import EntityRequest, AdditionRequest

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """
    Фикстура, которая читает и возвращает URL для API-сервиса
    """
    url = os.getenv("API_HOST")
    if not url:
        pytest.fail("Переменная окружения API_HOST не задана в .env файле")
    return f"{url}/api"


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Фикстура, которая создает и настраивает экземпляр API-клиента.
    """
    client = ApiClient(base_url=base_url)
    return client


@pytest.fixture
def new_entity_payload() -> EntityRequest:
    """Фикстура, генерирующая валидный payload для создания сущности."""
    return EntityRequest(
        title="Test Title",
        verified=True,
        important_numbers=[1, 2, 3],
        addition=AdditionRequest(
            additional_info="Test additional info", additional_number=42
        ),
    )
