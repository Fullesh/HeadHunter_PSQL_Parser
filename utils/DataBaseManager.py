import psycopg2
from psycopg2.errors import *


class DBManager:

    def __init__(self):
        self.connection = None
        self.conn_params = {'host': 'localhost',
                            'database': 'northwind',
                            'user': 'postgres',
                            'password': '1'}
        self.new_params = {'host': 'localhost',
                           'database': 'headhunter_database',
                           'user': 'postgres',
                           'password': '1'}

    def __repr__(self):
        return f'Параметры подключения к БД: {self.new_params} \n' \
               f'Существует ли БД: {self.check_databases()} \n' \
               f'Название БД: headhunter_database \n' \
               f'Пользователь БД: postgres'

    def open_con(self, connection_params):
        """
        Открывает подключение к БД
        :param connection_params: параметры для подключения
        :return: Открытое подключение
        """
        self.connection = psycopg2.connect(**connection_params)
        self.connection.autocommit = True
        return self.connection

    def check_databases(self):
        """
        Функция для проверки существует ли БД
        :return: True/False
        """
        try:
            self.open_con(self.new_params)
            print('Успешное подключение к БД headhunter_database')
            self.connection.close()
            return True
        except OperationalError:
            print('БД уже удалена либо ещё не существует, пропускаем...')

    def create_database(self):
        """
        Функция создает БД если её ещё не существует
        :return:
        """
        self.open_con(self.conn_params)
        with self.connection.cursor() as cur:
            try:
                cur.execute('create database headhunter_database')
            except DuplicateDatabase:
                print('База данных уже существует, пропускаем компанду')
        self.connection.close()

    def initialisation_of_tables(self):
        """
        Функция создаёт таблцы с работниками и вакансиями
        :return: None
        """
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            try:
                cur.execute("""create table employers (
                            id INT PRIMARY KEY,
                            employer_name varchar(100),
                            employer_url varchar(100),
                            open_vacancies INT )""")
                cur.execute("""create table vacancies (
                            id INT,
                            company varchar(100),
                            employer_url varchar(100),
                            salary_min int,
                            salary_max int,
                            city varchar(100),
                            vacancy_id int PRIMARY KEY,
                            vacancy_name varchar(100),
                            vacancy_url varchar(100))""")
            except DuplicateTable:
                print('Одна или обе таблицы существуют, пропускаем команду')
            finally:
                print('Успешно создали таблицы')
        self.connection.close()

    def append_employers_and_vacancies(self, employers, vacancies):
        """
        Функция добавляет в БД данные с работодателями и вакансиями
        :param employers: Словарь с данными о работодателях
        :param vacancies: Словарь с данными о вакансиях
        :return: None
        """
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            try:
                for employer in employers:
                    cur.execute('INSERT INTO employers VALUES(%s,%s,%s,%s)', (
                        employer['id'],
                        employer['employer_name'],
                        employer['employer_url'],
                        employer['open_vacancies']
                    ))
            except UniqueViolation:
                print('Таблица employers уже заполнена данные, либо имеются повторения в PrimaryKey')
            try:
                for vacancy in vacancies:
                    cur.execute('INSERT INTO vacancies VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                        vacancy['id'],
                        vacancy['company'],
                        vacancy['url'],
                        vacancy['salary_min'],
                        vacancy['salary_max'],
                        vacancy['city'],
                        vacancy['vacancies_id'],
                        vacancy['vacancies_name'],
                        vacancy['url_vacancies']
                    ))
            except UniqueViolation:
                print('Таблица vacancies уже заполнена данными либо имеет повторяющиеся значения PrimaryKey')
            self.connection.close()

    def get_companies_and_vacancies_count(self):
        """
        Вывод количество уникальных работодателей в БД и количество всех вакансий
        :return: Количество уникальных работодателей и количество вакансий
        """
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute('SELECT COUNT(DISTINCT employer_name) FROM employers')
            employers_count = cur.fetchone()
            cur.execute('SELECT COUNT(*) FROM vacancies')
            vacancies_count = cur.fetchone()
        self.connection.close()
        return employers_count, vacancies_count

    def get_all_vacancies(self):
        """
        Функция выводит информацию о всех вакансиях в БД
        :return:
        """
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute('SELECT company, vacancy_name, vacancy_url FROM VACANCIES')
            data = cur.fetchall()
            for line in data:
                print(line)
        self.connection.close()

    def get_avg_salary(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute('SELECT ROUND(AVG((salary_max + salary_min) / 2)) FROM vacancies')
            average_salary = cur.fetchone()
        self.connection.close()
        return average_salary

    def get_vacancies_with_keyword(self, keyword):
        """
        Вывод на экран все вакансии которые соответствуют введённому ключевому слову
        :param keyword: Ключевое слово
        :return: None
        """
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute(
                f"""
                SELECT company, vacancy_name, vacancy_url
                FROM vacancies
                WHERE vacancy_name like '%{keyword}%'
                """
            )
            data = cur.fetchall()
            for line in data:
                print(line)
        self.connection.close()

    def get_vacancies_with_higher_salary(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute(f"""
            SELECT company, salary_min, salary_max, vacancy_name, vacancy_url
            FROM vacancies
            WHERE (salary_min + salary_max) / 2 > {self.get_avg_salary()[0]}
            """)
            data = cur.fetchall()
            for line in data:
                print(line)
        self.connection.close()

    def delete_tables(self):
        """
        Функция удаляет таблицы с работодателями и вакансиями
        :return: None
        """
        try:
            self.open_con(self.new_params)
            with self.connection.cursor() as cur:
                cur.execute('DROP TABLE employers')
                cur.execute('DROP TABLE vacancies')
            print('Успешно удалили таблицу employers')
            print('Успешно удалили таблицу vacancies')
        except UndefinedTable:
            print('Таблиц уже не существует')

    def total_drop(self):
        """
        Полностью удаляет БД и таблцы в ней
        :return: None
        """
        try:
            self.open_con(self.new_params)
            with self.connection.cursor() as cur:
                cur.execute('DROP DATABASE headhunter_database with (FORCE)')
        except OperationalError:
            print('База данных уже удалена или ещё не существует, пропускаем...')
        self.delete_tables()
