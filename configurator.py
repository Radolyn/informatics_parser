import getpass
import os
import time

import utils
from informatics import Informatics
from settings import Settings

utils.initialize()


def welcome():
    utils.header('ДИСКЛЕЙМЕР')
    print(
        'Для использования программы Вам необходимо ввести свои логин и пароль от informatics\'а.'
    )
    print(
        'Ваши данные не отправляются никуда, кроме informatics\'а и шифруются локально.'
    )
    print('P.S. Ввод пароля не показывается.')
    utils.header('/ДИСКЛЕЙМЕР')

    username = input('Логин: ')
    password = getpass.getpass('Пароль: ')

    utils.header('ИНФОРМАЦИЯ')
    print(
        'Отличие пароля от пароля для настроек состоит в том, что 2-ой придётся вводить каждый раз при запуске программы.'
    )
    print('Конечно же, всё для безопасности Ваших решений :)')
    utils.header()

    settings_password = getpass.getpass('Пароль от настроек: ')

    utils.header('ПРОВЕРКА АВТОРИЗАЦИИ')

    result = Informatics().authorize(username, password, False)

    if not result:
        utils.header('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
        exit(1)

    utils.header('СОЗДАНИЕ ОБЪЕКТА')
    settings = Settings(username, password)

    utils.header('ШИФРОВАНИЕ И ЗАПИСЬ')
    settings.save(settings_password)

    utils.header('ГОТОВО')

    print('Теперь Вы можете пользоваться всеми фишками программы :)')


def configurator():
    utils.header('ЗАГРУЗКА')

    settings_password = getpass.getpass('Пароль от настроек: ')
    settings = Settings
    try:
        settings = Settings.load(settings_password)
    except:
        utils.header('НЕВЕРНЫЙ ПАРОЛЬ')

    while 1:
        utils.clear()

        utils.header('ТЕКУЩИЕ НАСТРОЙКИ')
        print('1. Логин: ' + settings.username)
        print('2. Пароль: ' + settings.password)

        print('\n\nw. Сохранить и выйти')
        print('q. Выйти без сохранения\n\n')

        utils.header()

        user_choice = input('Выбор: ')

        utils.header()

        if user_choice == 'w':
            result = Informatics().authorize(settings.username,
                                             settings.password)
            if not result:
                print('Неправильный логин или пароль!')
                time.sleep(2.5)
                continue
            settings.save(settings_password)
            exit(0)
        elif user_choice == 'q':
            exit(0)
        elif user_choice == '1':
            username = input('Логин: ')
            settings.username = username
        elif user_choice == '2':
            password = getpass.getpass('Пароль: ')
            settings.password = password


if os.path.exists('settings'):
    configurator()
else:
    welcome()
