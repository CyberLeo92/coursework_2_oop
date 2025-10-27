import abc
import json
import os
from typing import List

from src.vacancy import Vacancy


class AbstractVacancyStorage(abc.ABC):
    """ Интерфейс для хранилища вакансий (файлы/БД) """

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """ Добавление вакансии в файл """
        raise NotImplementedError

    @abc.abstractmethod
    def get_vacancies(self, criterion: str) -> List[Vacancy]:
        """
        Получение вакансий по критериям
        Возвращает список доменных объектов Vacancy
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """ Удаление вакансии из файла """
        raise NotImplementedError


class JSONVacancyStorage(AbstractVacancyStorage):
    """ Класс для работы с JSON-файлом """

    def __init__(self, filename: str) -> None:
        self.__filename: str = filename
        os.makedirs(os.path.dirname(self.__filename) or ".", exist_ok=True)

    def __load(self) -> list[dict]:
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def __save(self, data: list[dict]) -> None:
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """ Добавление вакансии в JSON файл """
        data = self.__load()
        if not any(item.get("url") == vacancy.url for item in data):
            data.append(vacancy.__dict__)
            self.__save(data)

    def get_vacancies(self, criterion: str) -> List[Vacancy]:
        """ Получение вакансий по критерию """
        data = self.__load()
        if not criterion:
            return [Vacancy(**item) for item in data]
        needle = criterion.lower()
        return [
            Vacancy(**item)
            for item in data
            if needle in str(item.get("description", "")).lower()
            or needle in str(item.get("title", "")).lower()
        ]

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """ Удаление вакансии из JSON файла """
        data = self.__load()
        new_data = [
            item for item in data
            if not (item.get("url") == vacancy.url and item.get("title") == vacancy.title)
        ]
        if len(new_data) != len(data):
            self.__save(new_data)
