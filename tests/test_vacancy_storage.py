import json
import os
import unittest
from tempfile import NamedTemporaryFile

from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


class TestJSONVacancyStorage(unittest.TestCase):
    def setUp(self):
        """ Создание временного файла как хранилище """
        tmp = NamedTemporaryFile(delete=False)
        self.temp_path = tmp.name
        tmp.close()
        self.storage = JSONVacancyStorage(self.temp_path)

    def tearDown(self):
        """ Удаление временного файла после тестов """
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)

    def test_add_and_deduplicate(self):
        """ Добавление вакансий без дублей (по URL) """
        vacancy_1 = Vacancy(
            "Программист", "Москва", "http://example.com/vacancy1", "100000", "150000", "Описание"
        )
        vacancy_2 = Vacancy(
            "Программист", "Москва", "http://example.com/vacancy1", "110000", "150000", "Дубликат по URL"
        )
        self.storage.add_vacancy(vacancy_1)
        self.storage.add_vacancy(vacancy_2)

        with open(self.temp_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], "http://example.com/vacancy1")

    def test_get_vacancies_all_and_filter(self):
        """ Возврат всех вакансий и фильтрация по описанию/названию """
        dev = Vacancy("Программист", "Москва", "http://example.com/v1", "100000", "150000", "Описание вакансии")
        design = Vacancy("Дизайнер", "СПб", "http://example.com/v2", "80000", "120000", "Описание дизайнера")
        self.storage.add_vacancy(dev)
        self.storage.add_vacancy(design)

        all_item = self.storage.get_vacancies("")
        self.assertEqual(len(all_item), 2)
        self.assertIsInstance(all_item[0], Vacancy)

        only_design = self.storage.get_vacancies("Дизайнер")
        self.assertEqual(len(only_design), 1)
        self.assertEqual(only_design[0].title, "Дизайнер")


    def test_remove_vacancy(self):
        """ Тестирование удаления вакансии по URL и title """
        vacancy = Vacancy(
            "Программист", "Москва", "http://example.com/vacancy1", "100000", "150000", "Описание"
        )
        self.storage.add_vacancy(vacancy)
        self.storage.remove_vacancy(vacancy)

        with open(self.temp_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(len(data), 0)
