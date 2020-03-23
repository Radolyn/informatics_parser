# coding=utf-8

import os
import re

import requests
from bs4 import BeautifulSoup


class Informatics(object):
    # https://github.com/InformaticsMskRu/informatics-mccme-ru/blob/master/pynformatics/utils/run.py
    class Strings:
        @staticmethod
        def get_string_status(s):
            return {
                "OK": "OK",
                "WA": "Неправильный ответ",
                "ML": "Превышение лимита памяти",
                "SE": "Security error",
                "CF": "Ошибка проверки, обратитесь к администраторам",
                "PE": "Неправильный формат вывода",
                "RT": "Ошибка во время выполнения программы",
                "TL": "Превышено максимальное время работы",
                "WT": "Превышено максимальное общее время работы",
                "SK": "Пропущено"
            }[s]

        @staticmethod
        def get_lang_ext_by_id(language_id):
            languages = {
                1: ".pas",
                2: ".c",
                3: ".cpp",
                8: ".dpr",
                23: ".py",
                24: ".pl",
                18: ".java",
                25: ".cs",
                26: ".rb",
                22: ".php",
                27: ".py",
                28: ".hs",
                30: ".pas",
                29: ".bas",
                31: ".1c"
            }
            return languages.get(language_id, str())

        @staticmethod
        def get_language_name_by_id(language_id):
            languages_names = {
                1: "Free Pascal 2.6.2",
                2: "GNU C 4.9",
                3: "GNU C++ 4.9",
                7: "Turbo Pascal",
                8: "Borland Delphi 6 - 14.5",
                9: "Borland C",
                10: "Borland C++",
                18: "Java JDK 1.7",
                22: "PHP 5.2.17",
                23: "Python 2.7",
                24: "Perl 5.10.1",
                25: "Mono C# 2.10.8.0",
                26: "Ruby 1.8.7",
                27: "Python 3.3",
                28: "Haskell GHC 7.4.2",
                29: "FreeBASIC 1.00.0",
                30: "PascalABC 1.8.0.496",
                31: "1C 8.3"
            }
            return languages_names.get(language_id, str())

        @staticmethod
        def get_status_by_id(status_id):
            return {
                0: "OK",
                1: "CE",
                2: "RE",
                3: "TL",
                4: "PE",
                5: "WA",
                6: "CF",
                7: "Partial",
                8: "AC",
                9: "Ignored",
                10: "Disqualified",
                11: "Pending",
                12: "ML",
                13: "Security error",
                14: "Style Violation",
                15: "Wall Time Limit Exceeded",
                16: "Pending Review",
                17: "Rejected",
                18: "Skipped",
                96: "Running...",
                98: "Compiling..."
            }[status_id]

    def __init__(self):
        # Ссылка на сайт (с слешем на конце)
        self.base_url = 'https://informatics.mccme.ru/'

        # Сссылка на back-end (с слешем на конце)
        self.backend_route = 'py/'

        # Сессия для всех запросов
        self.session = requests.session()

        # Произошла ли авторизация
        self.authorized = False

        # Кеш данных пользователя
        self.user_data = {}

        # Номер языка (Python3 - 27)
        self.language_id = 27

    @property
    def backend_url(self):
        """
        :return: Ссылка на back-end
        """
        return self.base_url + self.backend_route

    def request_json(self, url: str, method: str = 'get', files: dict = None, data: dict = None):
        result = self.session.request(method, self.backend_url + url, json=True, files=files, data=data, timeout=5)
        if result is None:
            return {'code': 400, 'error': 'Something bad happened'}

        return self.standartize(result.json())

    def authorize(self, username: str, password: str, initialize: bool = True):
        """
        Авторизовывает пользователя
        :param username: Логин
        :param password: Пароль
        :param initialize: Если да, то заполняет значение user_data текущего объекта
        :return: Успешная ли авторизация
        """
        response = self.session.post(self.base_url + 'login/index.php',
                                     data={
                                         'username': username.lower(),
                                         'password': password
                                     })
        if 'Вы зашли под именем' in response.text:
            self.authorized = True
            if initialize:
                self.get_user_data()
            return True
        return False

    def get_user_data(self):
        """
        Данные текущего пользователя
        :return: Лист с данными
        """
        if not self.authorized:
            return {'code': 400, 'error': 'Not authorized'}
        data = self.request_json('rating/get')['current_user_data']
        # response = self.session.get(
        #     'https://informatics.mccme.ru/py/')
        # data = json.loads(response.text)['current_user_data']
        self.user_data = data

        return self.user_data

    def update_authorization_state(self):
        """
        Обновляет значение authorized
        """
        if self.get_user_data() is None:
            self.authorized = False
        else:
            self.authorized = True

    def get_problem_runs_by_user(self,
                                 problem_id: int,
                                 user_id: int,
                                 status_id: int = -1):
        """
        Получает посылки пользователя
        :param problem_id: Номер задания
        :param user_id: ID пользователя
        :param status_id: Статус посылок
        :return: Первые 100 посылок
        """
        result = self.request_json('problem/%i/filter-runs?problem_id=%i&user_id=%i&lang_id=%i&status_id=%i&count=100'
                                   '&page=1' %
                                   (problem_id, problem_id, user_id, self.language_id, status_id))

        if result['code'] != 200:
            return {'code': result['code']}

        return result['data']

    def get_problem_runs(self, problem_id: int, status_id: int = -1):
        """
        Получает посылки текущего пользователя
        :param problem_id: Номер задания
        :param status_id: Статус посылок
        :return: Первые 100 посылок
        """
        if not self.authorized:
            return {'code': 400, 'error': 'Not authorized'}
        return self.get_problem_runs_by_user(problem_id, self.user_data['id'],
                                             status_id)

    @staticmethod
    def str_cleaner(string: str):
        """
        Заменяет все двойные переходы и пробелы на одинарные
        :param string: Строка
        :return: Чистая строка
        """
        return re.sub(r'[\r\t]', '',
                      string).replace('    ',
                                      '').replace('\n \n',
                                                  '\n').replace('\n\n',
                                                                '\n')[:-1]

    def upload_solution(self, problem_id: int, file_path: str):
        """
        Загружает решение задания
        :param problem_id: Номер задания
        :param file_path: Путь к файлу
        :return: Объект с успешностью отправки и run_id
        """
        if not os.path.exists(file_path) or not self.authorized:
            return {'code': 400, 'error': 'File not found'}

        f = open(file_path, 'rb')
        response = self.request_json('problem/%i/submit' % problem_id,
                                     files={'file': f},
                                     data={'lang_id': self.language_id})

        # Стандартизируем ответ
        # if response['status'] == 'success':
        #     response['code'] = 200
        #     del response['status_code']

        return response

    @staticmethod
    def standartize(response):
        """
        Стандартизирует ответ
        :param response: json ответ
        :return: Стандартизированный ответ
        """
        if 'status_code' in response:
            response['code'] = response['status_code']
            del response['status_code']
        if 'result' in response:
            if response['result'] == 'success':
                response['code'] = 200
            else:
                response['code'] = 400
            del response['result']
        return response

    def get_run_by_id(self, run_id: int):
        """
        Получает информацию о посылке по ID
        :param run_id: ID посылки
        :return: Вся информация + исходный код
        """
        result = self.request_json('problem/run/%i/source' % run_id)

        if result['code'] != 200:
            return {'code': result['code']}

        return result['data']

    def get_problem_data(self, problem_id: int, detailed: bool = False):
        """
        Получает информацию по заданию
        :param problem_id: Номер задания
        :param detailed: Нужна ли полная информация (вся-вся, как на странице)
        :return: Информация о задании
        """
        # if not self.authorized:
        #    return None

        response = self.session.get(self.base_url +
                                    'mod/statements/view3.php?chapterid=%i' %
                                    problem_id)

        # TODO: Сделать проверку на "Вы не состоите в курсе"
        if response.status_code != 200:
            return None

        problem = {}

        tree = BeautifulSoup(response.text, 'html.parser')

        problem['id'] = problem_id

        problem['full_name'] = tree.find('div', {
            'class': 'statements_chapter_title'
        }).contents[0]

        problem['name'] = problem['full_name'].replace(
            'Задача №%i. ' % problem_id, '')

        desc_tree = tree.find('div', {
            'class': 'legend'
        })

        # Эти ваши информатиксы меня совсем не впечатляют
        if desc_tree:
            desc_tree = desc_tree.contents
            if len(desc_tree) >= 2:
                problem['description'] = self.str_cleaner(desc_tree[1].text)
            else:
                for item in desc_tree:
                    if len(item) > 14:
                        problem['description'] = self.str_cleaner(str(item))
                        break
                else:
                    problem['description'] = 'Не удалось получить описание'
        else:
            problem['description'] = 'Без описания'

        if not detailed:
            return problem

        problem['input_data'] = tree.find('div',
                                          {'class': 'input-specification'})

        if not problem['input_data'] is None:
            problem['input_data'] = self.str_cleaner(
                problem['input_data'].contents[3].text)

        problem['output_data'] = tree.find('div',
                                           {'class': 'output-specification'})

        if not problem['output_data'] is None:
            problem['output_data'] = self.str_cleaner(
                problem['output_data'].contents[3].text)

        # TODO: Можно спарсить таблицу "идеальных решений", а ещё ограничения по памяти и времени

        return problem
