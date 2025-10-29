from abc import ABC, abstractmethod

import requests


class AbstractVacancyAPI(ABC):
    """ Абстрактный класс для работы с API внешних сервисов """

    @abstractmethod
    def fetch_vacancies(self, *args, **kwargs):
        """ Абстрактный метод получения вакансий """
        pass


class HHVacancyAPI(AbstractVacancyAPI):
    """ Класс для работы с API hh.ru """

    def __init__(self):
        """ Инициализация атрибутов класса """
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__area_url = "https://api.hh.ru/areas"

    def __connect(self, url: str, *, params: dict | None = None) -> dict | list | None:
        """ Единая точка подключения к API (приватная). Возвращает JSON или None """
        try:
            rest = requests.get(url, params=params, timeout=5)
            rest.raise_for_status()
            return rest.json()
        except requests.RequestException as e:
            print("Ошибка при подключение к API:", e)
            return None

    def fetch_vacancies(self, search_query: str, area: str = "", page: int = 0, per_page: int = 20):
        """Получение вакансий на hh.ru (формирует params, вызывает __connect, парсит items)."""
        area_id = self.__fetch_area_id(area)
        params = {"text": f"NAME:{search_query}", "area": area_id, "page": page, "per_page": per_page}
        data = self.__connect(self.__base_url, params=params)
        if isinstance(data, dict):
            return data.get("items", [])
        return []

    def __fetch_area_id(self, user_area: str):
        """Поиск кода региона/города на hh.ru (приватный)."""
        data_list = self.__connect(self.__area_url)
        if not isinstance(data_list, list):
            return None

        for regions in data_list:
            areas = regions.get("areas")
            if not isinstance(areas, list):
                continue
            for region in areas:
                if region.get("name") == user_area:
                    return int(region["id"])
                if region.get("areas"):
                    for area in region["areas"]:
                        if area.get("name") == user_area:
                            return int(area["id"])
        return None
