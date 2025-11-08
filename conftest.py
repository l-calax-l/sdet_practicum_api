import pytest
import os
from dotenv import load_dotenv
from src.api_client import ApiClient

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """
    Фикстура, которая читает и возвращает URL для API-сервиса
    из BASE_URL.
    """
    url = os.getenv("BASE_URL")
    if not url:
        pytest.fail("Переменная окружения BASE_URL не задана в .env файле")
    return url


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Фикстура, которая создает и настраивает экземпляр API-клиента.
    """
    client = ApiClient(base_url=base_url)
    return client