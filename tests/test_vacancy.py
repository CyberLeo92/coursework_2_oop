import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_initialization(self):
        """ Создание объекта и приведение зарплаты к int """
        vacancy = Vacancy(
            title="Разработчик Python",
            area="Москва",
            url="http://example.com/vacancy/1",
            salary_from="0",
            salary_to="120000",
            description="Заниматься разработкой на Python.",
        )

        self.assertEqual(vacancy.title, "Разработчик Python")
        self.assertEqual(vacancy.area, "Москва")
        self.assertEqual(vacancy.url, "http://example.com/vacancy/1")
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 120000)
        self.assertEqual(vacancy.description, "Заниматься разработкой на Python.")

    def test_str_method(self):
        """ Проверяет работу метода __str__ (диапазон зарплаты) """
        vacancy = Vacancy(
            title="Разработчик Python",
            area="Москва",
            url="http://example.com/vacancy/1",
            salary_from="0",
            salary_to="120000",
            description="",
        )

        expected_str = "Разработчик Python — Москва. Зарплата: 120000. Ссылка: http://example.com/vacancy/1"
        self.assertEqual(str(vacancy), expected_str)

    def test_lt_method(self):
        """ Сортировка по зарплате """
        vacancy_1 = Vacancy(
            title="Junior", area="Москва", url="url_1", salary_from="0", salary_to="60000", description=""
        )
        vacancy_2 = Vacancy(
            title="Senior", area="Москва", url="url_2", salary_from="0", salary_to="120000", description=""
        )

        self.assertTrue(vacancy_1 < vacancy_2)
        self.assertFalse(vacancy_2 < vacancy_1)

    def test_validation_raises(self):
        """ Пустые title или url -> ValueError """
        with self.assertRaises(ValueError):
            Vacancy("", "Спб", "http://example.com", "10000", "20000", "")
        with self.assertRaises(ValueError):
            Vacancy("Dev", "Спб", "", "10000", "20000", "")
