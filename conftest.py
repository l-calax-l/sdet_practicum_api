import pytest
import os
from dotenv import load_dotenv
from src.api_client import ApiClient
from helpers import data_generator

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
def created_entity(api_client: ApiClient):
    """
    Фикстура для создания и последующей очистки одной сущности.
    1. Создает сущность с данными по умолчанию.
    2. Передает ID и payload созданной сущности в тест.
    3. Гарантированно удаляет сущность после завершения теста.
    """
    payload = data_generator.default_entity()
    create_response = api_client.create_entity(payload)

    assert (
        create_response.status_code == 200
    ), "Предусловие не выполнено: не удалось создать сущность"
    entity_id = int(create_response.text)

    yield {"id": entity_id, "payload": payload}

    api_client.delete_entity(entity_id)


@pytest.fixture
def created_entities_for_filter_test(api_client):
    """
    Фикстура для теста фильтрации:
    1. Создает одну verified и одну unverified сущность.
    2. Передает их ID и заголовки в тест.
    3. Гарантированно удаляет обе сущности после завершения теста.
    """
    entities_to_delete = []

    verified_payload = data_generator.verified_entity()
    unverified_payload = data_generator.unverified_entity()

    create_verified_res = api_client.create_entity(verified_payload)
    assert (
            create_verified_res.status_code == 200
    ), "Не удалось создать 'verified' сущность для теста"
    verified_id = int(create_verified_res.text)
    entities_to_delete.append(verified_id)

    create_unverified_res = api_client.create_entity(unverified_payload)
    assert (
            create_unverified_res.status_code == 200
    ), "Не удалось создать 'unverified' сущность для теста"
    unverified_id = int(create_unverified_res.text)
    entities_to_delete.append(unverified_id)

    yield {
        "verified_id": verified_id,
        "unverified_id": unverified_id,
        "unverified_title": unverified_payload.title,
    }

    for entity_id in entities_to_delete:
        api_client.delete_entity(entity_id)
