# coding=utf-8
# Here we go again

import argparse
import informatics
import utils
from settings import Settings
import yapf
import getpass
import autopep8
import os


problems, folder = utils.args_parser()

if not problems:
    print('Не указаны задания для обработки')
    exit(130)

if not os.path.exists(folder):
    os.mkdir(folder)

utils.header('ВХОД')

if not os.path.exists('settings'):
    print('Запустите сначала configurator.py')
    utils.header('/ВХОД')
    exit(1)

password = getpass.getpass('Пароль от настроек: ')

try:
    settings = Settings.load(password)
except:
    print('Неправильный пароль')
    utils.header('/ВХОД')
    exit(1)

inf = informatics.Informatics()

inf.authorize(settings.username, settings.password)

if not inf.authorized:
    print('Неправильный логин или пароль!')
    utils.header('/ВХОД')
    exit(1)

print('Доброго времени суток, ' + inf.user_data['name'])

utils.header('/ВХОД')

utils.header('ОБРАБОТКА')

problems_handled = 0

for problem_id in problems:
    problem_data = inf.get_problem_data(problem_id)

    utils.header(problem_data['full_name'])

    # удачные попытки
    user_runs = inf.get_problem_runs(problem_id, 0)

    if not user_runs:
        utils.header('НЕТ УДАЧНЫХ ПОПЫТОК')
        continue

    run = inf.get_run_by_id(user_runs[0]['id'])
    description = problem_data['description'].replace('\n', '\n# ')
    source = '# ' + problem_data[
        'full_name'] + '\n# ' + description + '\n\n' + run['source']

    # форматируем код
    try:
        formatted_source = yapf.yapf_api.FormatCode(source,
                                                    style_config='pep8',
                                                    verify=True)[0]
        fixed_source = autopep8.fix_code(formatted_source,
                                         options={'aggressive': 2})
    except:
        print('Не удалось отформатировать код. Возможно, не Python')
        fixed_source = source

    f = open(
        folder + os.path.sep + problem_data['name'] +
        inf.Strings.get_lang_ext_by_id(run['language_id']), 'w')
    f.write(fixed_source)
    f.close()

    problems_handled += 1

    utils.header('ЗАПИСАНО')

utils.header('/ОБРАБОТКА')

utils.header('ИТОГ')

print('Обработано заданий: %i из %i' % (problems_handled, len(problems)))

utils.header('/ИТОГ')
