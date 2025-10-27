import unittest
from unittest.mock import Mock, patch

from src.vacancy_api import HHVacancyAPI


class TestHHVacancyAPI(unittest.TestCase):

    @patch("src.vacancy_api.requests.get")
    def test_fetch_area_id(self, mock_get):
        """ Проверяем поиск area_id внутри __fetch_area_id (Москва/СПБ) """
        # ответ для https://api.hh.ru/areas
        areas_resp = Mock()
        areas_resp.status_code = 200
        areas_resp.json.return_value = [
            {
                "areas": [
                    {"name": "Москва", "id": "1", "areas": []},
                    {
                        "name": "Санкт-Петербург",
                        "id": "2",
                        "areas": [
                            {"name": "Центральный", "id": "3", "areas": []},
                            {"name": "Петроградский", "id": "4", "areas": []},
                        ],
                    },
                ]
            }
        ]
        mock_get.return_value = areas_resp

        api = HHVacancyAPI()

        # Тестируем поиск по области "Москва"
        area_id = api._HHVacancyAPI__fetch_area_id("Центральный") # type: ignore
        self.assertEqual(area_id, 3)

        # тестируем поиск по области, которая не существует
        area_id = api._HHVacancyAPI__fetch_area_id("Несуществующий район") # type: ignore
        self.assertIsNone(area_id)

    @patch("src.vacancy_api.requests.get")
    def test_fetch_vacancies_success_and_error(self, mock_get):
        """ Проверяем успешный (200) и неуспешный (не 200) сценарий fetch_vacancies"""
        api = HHVacancyAPI()

        # подготавливаем два разных ответа: сначала для areas, затем для vacancies
        areas_resp = Mock()
        areas_resp.status_code = 200
        areas_resp.json.return_value = [{"areas": [{"name": "Москва", "id": "1", "areas": []}]}]

        # Тест получения вакансий
        vacancies_resp_ok = Mock()
        vacancies_resp_ok.status_code = 200
        vacancies_resp_ok.json.return_value = {
            "items": [{"id": "x1", "name": "Вакансия 1"}, {"id": "x2", "name": "Вакансия 2"}]
        }

        # Проверяем отрицательный сценарий на статус 404
        vacancies_resp_fail = Mock()
        vacancies_resp_fail.status_code = 404

        def side_effect(url, *args, **kwargs):
            """ Чтоб разные вызовы requests.get возвращали разные ответы """
            if "areas" in url:
                return areas_resp
            return vacancies_resp_ok

        mock_get.side_effect = side_effect
        items = api.fetch_vacancies("разработчик", "Москва", 0, 10)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["name"], "Вакансия 1")

        def side_effect_fail(url, *args, **kwargs):
            """ Имитация ошибки при запросе вакансий """
            if "areas" in url:
                return areas_resp
            return vacancies_resp_fail

        mock_get.side_effect = side_effect_fail
        items = api.fetch_vacancies("разработчик", "Москва", 0, 10)
        self.assertEqual(items, [])
