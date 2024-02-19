import requests as rq
import requests.exceptions


class Parser:

    def __init__(self):
        self.employeers_data = []
        self.parsed_vacancies = []
        self.vacancies_data = []
        self.employers_ids = []
        self.employers_info = []

    def __repr__(self):
        return f"Employers ID's is: {self.employers_ids} \n" \
               f"Founded vacancies: {self.parsed_vacancies} \n" \
               f"Founded vacancies in total: {len(self.parsed_vacancies)}"

    def get_employers(self, request):
        for query in request:
            params = dict(text=query, only_with_vacancies=True, per_page=100)
            response = rq.get('https://api.hh.ru/employers', params=params)
            self.employeers_data.append(response.json())
        for employer in self.employeers_data:
            self.employers_ids.append(employer['items'][0]['id'])
            self.employers_info.append({
                'id': employer['items'][0]['id'],
                'employer_name': employer['items'][0]['name'],
                'employer_url': employer['items'][0]['url'],
                'open_vacancies': employer['items'][0]['open_vacancies']
            })
        return self.employeers_data, self.employers_ids, self.employers_info

    @staticmethod
    def get_salary(salary):
        salary_list = [0, 0]
        if salary and salary['from'] and salary['from'] != 0:
            salary_list[0] = salary['from']
        if salary and salary['to'] and salary['to'] != 0:
            salary_list[1] = salary['to']
        return salary_list

    def get_vacancies(self):
        params = {
            "employer_id": self.employers_ids,
            "per_page": 100,
            "only_with_salary": True
        }
        try:
            response = rq.get('https://api.hh.ru/vacancies', params=params)
            return self.get_data(response.json())
        except requests.exceptions.HTTPError:
            print('Подключение не удалось')

    def get_data(self, data):
        for vacancy_info in data['items']:
            salary_from, salary_to = self.get_salary(vacancy_info['salary'])
            self.parsed_vacancies.append({
                'id': vacancy_info['employer']['id'],
                'company': vacancy_info['employer']['name'],
                'url': vacancy_info['employer']['url'],
                'salary_min': salary_from,
                'salary_max': salary_to,
                'city': vacancy_info['area']['name'],
                'vacancies_id': vacancy_info['id'],
                'vacancies_name': vacancy_info['name'],
                'url_vacancies': vacancy_info['alternate_url']
            })
        return self.parsed_vacancies



