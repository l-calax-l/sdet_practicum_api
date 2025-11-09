import allure
import json
import requests
from requests import Response
from src.models import EntityRequest
from src.endpoints import ApiEndpoints


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _log_request(self, response: Response):
        """Прикрепляет детальную информацию о запросе и ответе к отчету Allure."""
        try:

            allure.attach(
                f"{response.request.method} {response.request.url}",
                "Request URL",
                allure.attachment_type.TEXT,
            )

            if response.request.body:
                allure.attach(
                    json.dumps(
                        json.loads(response.request.body), indent=2, ensure_ascii=False
                    ),
                    "Request Body",
                    allure.attachment_type.JSON,
                )

            allure.attach(
                f"Status Code: {response.status_code}",
                "Response Status Code",
                allure.attachment_type.TEXT,
            )
            if response.text:
                allure.attach(
                    json.dumps(response.json(), indent=2, ensure_ascii=False),
                    "Response Body",
                    allure.attachment_type.JSON,
                )
        except (json.JSONDecodeError, AttributeError):

            allure.attach(
                response.text, "Response Body (Text)", allure.attachment_type.TEXT
            )
        except Exception as e:
            allure.attach(
                f"Ошибка при логировании: {e}",
                "Logging Error",
                allure.attachment_type.TEXT,
            )

    def create_entity(self, payload: EntityRequest) -> Response:
        url = f"{self.base_url}{ApiEndpoints.CREATE_ENTITY}"
        response = requests.post(url, json=payload.model_dump())
        self._log_request(response)
        return response

    def get_entity(self, entity_id: int) -> Response:
        url = f"{self.base_url}{ApiEndpoints.get_entity_by_id(entity_id)}"
        response = requests.get(url)
        self._log_request(response)
        return response

    def get_all_entities(self, params: dict = None) -> Response:
        url = f"{self.base_url}{ApiEndpoints.GET_ALL_ENTITIES}"
        response = requests.get(url, params=params)
        self._log_request(response)
        return response

    def update_entity(self, entity_id: int, payload: EntityRequest) -> Response:
        url = f"{self.base_url}{ApiEndpoints.update_entity_by_id(entity_id)}"
        response = requests.patch(url, json=payload.model_dump())
        self._log_request(response)
        return response

    def delete_entity(self, entity_id: int) -> Response:
        url = f"{self.base_url}{ApiEndpoints.delete_entity_by_id(entity_id)}"
        response = requests.delete(url)
        self._log_request(response)
        return response
