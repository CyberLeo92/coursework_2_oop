import os

from src.vacancy_api import HHVacancyAPI
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


def main() -> None:
    """ Функция взаимодействия с пользователем """
    api = HHVacancyAPI()
    path = os.path.join(os.path.dirname(__file__), "data", "vacancy.json")
    storage = JSONVacancyStorage(path)

    region_choice = input("Введите населенный пункт(город, регион и т.п.): ")
    while True:
        print("\n1. Поиск вакансий")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии по ключевому слову в описании")
        print("4. Выход из программы")
        choice = input("\nВыберите действие: ")

        if choice == "1":
            query = input("Введите название вакансии: ")
            for item in api.fetch_vacancies(query, region_choice):
                vacancy = Vacancy.from_hh_item(item)
                print(vacancy)
                storage.add_vacancy(vacancy)

        elif choice == "2":
            top_amount = input("Введите количество топ-вакансий: ")
            if not top_amount.isdigit():
                print("Вы ввели не число")
                continue
            all_vacancies = storage.get_vacancies("")
            top_vacancies = sorted(all_vacancies, reverse=True)
            if len(top_vacancies) >= int(top_amount):
                for vacancy in top_vacancies[:int(top_amount)]:
                    print(vacancy)
            else:
                print("Общее количество вакансий меньше количества запроса")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ")
            for vacancy in storage.get_vacancies(keyword):
                print(vacancy)

        elif choice == "4":
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
