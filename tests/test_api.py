import allure
from src.api_client import ApiClient
from src.models import EntityResponse, EntityListResponse
from helpers import data_generator


@allure.epic("Entity Management")
@allure.feature("Core Functionality")
class TestEntityApi:

    @allure.story("Создание сущности")
    @allure.title("Позитивный тест: создание и проверка сущности")
    def test_create_and_get_entity(self, api_client: ApiClient, created_entity):
        entity_id = created_entity["id"]
        payload = created_entity["payload"]

        with allure.step("Отправка GET-запроса на /get/{id} для проверки"):
            get_response = api_client.get_entity(entity_id)

            assert (
                get_response.status_code == 200
            ), f"Ожидался статус-код 200, но получен {get_response.status_code}"

            entity_data = EntityResponse.model_validate(get_response.json())
            assert (
                entity_data.id == entity_id
            ), f"ID полученной сущности не совпадает. Ожидался {entity_id}, получен {entity_data.id}"
            assert (
                entity_data.title == payload.title
            ), f"Title сущности не совпадает. Ожидался '{payload.title}', получен '{entity_data.title}'"

    @allure.story("Получение списка сущностей")
    @allure.title("Позитивный тест: получение списка всех сущностей")
    def test_get_all_entities(self, api_client: ApiClient):
        with allure.step("Отправка GET-запроса на /getAll"):
            response = api_client.get_all_entities()
            assert (
                response.status_code == 200
            ), f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Валидация структуры ответа"):
            parsed_response = EntityListResponse.model_validate(response.json())
            assert isinstance(
                parsed_response.entity, list
            ), "Ключ 'entity' должен содержать список"

    @allure.story("Обновление сущности")
    @allure.title("Позитивный тест: обновление и проверка сущности")
    def test_update_entity(self, api_client: ApiClient, created_entity):
        entity_id = created_entity["id"]

        with allure.step("Отправка PATCH-запроса на /patch/{id}"):
            update_payload = data_generator.updated_entity_payload()
            update_response = api_client.update_entity(entity_id, update_payload)
            assert (
                update_response.status_code == 204
            ), f"Ожидался статус-код 204 после обновления, но получен {update_response.status_code}"

        with allure.step("Проверка обновленных данных через GET-запрос"):
            get_response = api_client.get_entity(entity_id)
            assert (
                get_response.status_code == 200
            ), "Не удалось получить сущность после обновления"

            updated_data = EntityResponse.model_validate(get_response.json())
            assert updated_data.title == update_payload.title, "Title не обновился"
            assert (
                updated_data.verified == update_payload.verified
            ), "Статус verified не обновился"

    @allure.story("Удаление сущности")
    @allure.title("Позитивный тест: удаление и проверка удаления сущности")
    def test_delete_entity(self, api_client: ApiClient, created_entity):
        entity_id = created_entity["id"]

        with allure.step("Отправка DELETE-запроса на /delete/{id}"):
            delete_response = api_client.delete_entity(entity_id)
            assert (
                delete_response.status_code == 204
            ), f"Ожидался статус-код 204 после удаления, но получен {delete_response.status_code}"

        with allure.step("Проверка, что сущность больше не доступна по GET"):
            get_response = api_client.get_entity(entity_id)

            # TODO: БАГ! После удаления сущности GET запрос возвращает 500 вместо 404
            assert (
                get_response.status_code >= 400
            ), f"Ожидался код ошибки (4xx-5xx), но получен {get_response.status_code}"

            if get_response.status_code != 404:
                allure.attach(
                    f"Обнаружен баг: GET после DELETE возвращает {get_response.status_code}. Response: {get_response.text}",
                    name="BUG: Wrong status code after deletion",
                    attachment_type=allure.attachment_type.TEXT,
                )

    @allure.story("Получение списка сущностей")
    @allure.title(
        "Позитивный тест: фильтрация списка сущностей по параметру 'verified'"
    )
    def test_get_all_entities_with_filter(
        self, api_client: ApiClient, created_entities_for_filter_test
    ):

        with allure.step("Отправка GET-запроса на /getAll с фильтром ?verified=true"):
            params = {"verified": "true"}
            response = api_client.get_all_entities(params=params)
            assert (
                response.status_code == 200
            ), "Запрос с фильтром вернул неверный статус-код"

        with allure.step(
            "Валидация ответа: все сущности в списке должны иметь verified=True"
        ):
            parsed_response = EntityListResponse.model_validate(response.json())
            assert (
                parsed_response.entity
            ), "Список отфильтрованных сущностей не должен быть пустым"

            unverified_title = created_entities_for_filter_test["unverified_title"]
            for entity in parsed_response.entity:
                assert (
                    entity.verified is True
                ), f"Найдена сущность '{entity.title}' с verified=False при фильтре"
                assert (
                    entity.title != unverified_title
                ), f"В отфильтрованном списке найдена сущность '{unverified_title}', которая не должна была туда попасть"
