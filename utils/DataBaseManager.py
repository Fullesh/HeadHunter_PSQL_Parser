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
        pass

    def open_con(self, connection_params):
        self.connection = psycopg2.connect(**connection_params)
        self.connection.autocommit = True
        return self.connection

    def create_database(self):
        self.open_con(self.conn_params)
        with self.connection.cursor() as cur:
            try:
                cur.execute('create database headhunter_database')
            except DuplicateDatabase:
                print('База данных уже существует, пропускаем компанду')
        self.connection.close()

    def initialisation_of_tables(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            try:
                cur.execute("""create table employers (
                            id INT PRIMARY KEY,
                            employer_name varchar(100),
                            employer_url varchar(100),
                            open_vacancies INT )""")
                cur.execute("""create table vacancies (
                            id INT PRIMARY KEY,
                            company varchar(100),
                            employer_url varchar(100),
                            salary_min int,
                            salary_max int,
                            city varchar(100),
                            vacancy_id int,
                            vacancy_name varchar(100),
                            vacancy_url varchar(100))""")
            except DuplicateTable:
                print('Одна или обе таблицы существуют, пропускаем команду')

    def append_employers_and_vacancies(self, employers, vacancies):
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

    def get_companies_and_vacancies_count(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            pass

    def get_all_vacancies(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM VACANCIES')
            data = cur.fetchall()
            for line in data:
                print(line)

    def get_avg_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword):
        pass

    def clear_tables(self):
        self.open_con(self.new_params)
        with self.connection.cursor() as cur:
            cur.execute('TRUNCATE TABLE employers')
            cur.execute('TRUNCATE TABLE vacancies')
        print('Успешно очистили таблицу employers')
        print('Успешно очистили таблицу vacancies')
