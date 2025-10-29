from __future__ import annotations
from typing import Optional


class Vacancy:
    """
    Класс, описывающий вакансию. Используется для хранения и сравнения данных.
    :arg title - заголовок вакансии
    :arg area - населенный пункт (город, регион, и т.д.)
    :arg url - ссылка на вакансию
    :arg salary_from - зарплата от...
    :arg salary_to - зарплата до...
    :arg description - описание вакансии
    """

    __slots__ = ("title", "area", "url", "salary_from", "salary_to", "description")

    def __init__(
            self,
            title: str,
            area: str,
            url: str,
            salary_from: Optional[str | int],
            salary_to: Optional[str | int],
            description: str
    ) -> None:
        self._validate_title_and_url(title, url)

        self.title: str = (title or "").strip()
        self.area: str = (area or "").strip()
        self.url: str = (url or "").strip()

        # Нормализую зарплату к int; пустые значения -> 0
        self.salary_from: int = self._coerce_salary(salary_from)
        self.salary_to: int = self._coerce_salary(salary_to)
        if self.salary_to < self.salary_from:
            self.salary_to = self.salary_from

        self.description: str = (description or "").strip()

    def __str__(self) -> str:
        if self.salary_from and self.salary_to:
            diapason = f"от {self.salary_from} до {self.salary_to}"
        else:
            diapason = str(self.salary_to or self.salary_from or 0)
        return f"{self.title} — {self.area}. Зарплата: {diapason}. Ссылка: {self.url}"

    def _salary_key(self) -> int:
        return self.salary_to or self.salary_from or 0

    def __lt__(self, other: "Vacancy") -> bool:
        """ Сравнение вакансий выполняется по зарплате для сортировки """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary_key() < other._salary_key()

    def __eq__(self, other: object) -> bool:
        """ Сравнение вакансий выполняется по URL для проверки равенства """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.url == other.url

    @staticmethod
    def _validate_title_and_url(title: str, url: str) -> None:
        if not title or not title.strip() or not url or not url.strip():
            raise ValueError("Название и ссылка на вакансию обязательны.")

    @staticmethod
    def _coerce_salary(value: Optional[str | int]) -> int:
        """ Для приведения зарплаты к int"""
        if value is None:
            return 0
        if isinstance(value, int):
            return max(value, 0)
        s = str(value).strip()
        s = s.replace(" ", "")
        return int(s) if s.isdigit() else 0

    @classmethod
    def from_hh_item(cls, item: dict) -> "Vacancy":
        """ Превращает элемент ответа hh.ru в Vacancy (чтоб не дублировать логику в main.py) """
        name = item.get("name", "")
        area = (item.get("area") or {}).get("name", "")
        url = item.get("alternate_url", "")
        snippet = (item.get("snippet") or {}).get("requirement", "") or ""
        salary = item.get("salary") or {}
        return cls(
            title=name,
            area=area,
            url=url,
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            description=snippet,
        )
