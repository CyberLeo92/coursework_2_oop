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

    def fetch_vacancies(self, search_query: str, area: str = "", page: int = 0, per_page: int = 20):
        """Метод получения вакансий на сайте hh.ru
        :arg search_query - поисковый запрос,
        :arg area - название населенного пункта,
        :arg page - номер страницы,
        :arg per_page - количество элементов на странице"""

        area_id = self.__fetch_area_id(area)
        params = {"text": f"NAME:{search_query}", "area": area_id, "page": page, "per_page": per_page}

        response = requests.get(self.__base_url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return []

    def __fetch_area_id(self, user_area: str):
            """ Метод поиска кода региона, населенного пункта или города на сайте hh.ru """
            response = requests.get(self.__area_url)
            if response.status_code == 200:
                data_list = response.json()

                if not isinstance(data_list, list):
                    print("Ошибка: ожидает список, но получен:", type(data_list))
                    return None

                for regions in data_list:
                    if "areas" not in regions or not isinstance(regions["areas"], list):
                        print("Ошибка: в элементе отсутствует ключ 'areas' или он не является списком:", regions)
                        continue

                    for region in regions["areas"]:
                        if region["name"] == user_area:
                            return int(region["id"])
                        elif not region["areas"]:
                            continue
                        for area in region["areas"]:
                            if area["name"] == user_area:
                                return int(area["id"])
            else:
                print("Ошибка при получении данных: ", response.status_code)
                return None
