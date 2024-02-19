from utils.hh_parser import Parser
from utils.DataBaseManager import DBManager
import os


request = []
employers = []
parser_data = Parser()
database_worker = DBManager()
check_restart = 'n'


def check_bool_input(answer):
    """
    Функция проверяет положительный или отрицательный ответ ввёл пользователь
    :param answer: Ответ пользователя
    :return: True/False в зависимости от ответа
    """
    return answer.lower() in ['y', 'yes', 'да']


database_worker.__repr__()
print('Проверяем существование БД на локальной машине, пожлауйста подождите...')
check_database = database_worker.check_databases()
if check_database and os.path.exists('config.txt') is True:
    print('Всё хорошо, продолжаем')
elif os.path.exists('config.txt') is False and check_database is True:
    print('Конфигурация отсутствует, БД присутствует, исправляем...')
    database_worker.total_drop()
else:
    print('Всё проверили, начинаем')


def init_database(worker):
    """
    Инициализируем БД и таблцы
    :param worker: Экземпляр класса DBManager
    :return: None
    """
    worker.create_database()
    worker.initialisation_of_tables()


def from_scratch():
    """
    Фукнция позволяет простым вызовом начать заполнение данных с нуля
    :return: Список работодателей
    """
    query = input('Введите имя компаний через пробел, до 10 шутк: ')
    with open('config.txt', 'w') as conf_file:
        vacancies_list = query.lower().split()
        if len(vacancies_list) > 10:
            print('Введено больше 10 вакансий')
            exit(0)
        else:
            for employer in vacancies_list:
                conf_file.write(employer + ' ')
                _, _, employers_list = parser_data.get_employers(vacancies_list)
    return employers_list


if os.path.exists('config.txt'):
    check_restart = input('Вижу файл конфигурации. Продолжаем двигаться с ним?[y/n] ')
    if check_bool_input(check_restart) is False:
        employers = from_scratch()
    else:
        database_worker.delete_tables()
        with open('config.txt', 'r') as cfg_file:
            request = cfg_file.readline().split()
            if len(request) != 0:
                _, _, employers = parser_data.get_employers(request)
            else:
                print('Файл конфигурации пуст!')
else:
    employers = from_scratch()
    init_database(database_worker)

vacancies = parser_data.get_vacancies()
database_worker.initialisation_of_tables()
database_worker.append_employers_and_vacancies(employers, vacancies)
