import argparse
import os

letters_list = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC',
    'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO',
    'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ'
]


def header(msg: str = ''):
    print('\n--- ' + msg.upper() + ' ---\n')


def extend_list(_list, _range):
    for r in _range:
        start, end = r.split('-')
        for i in range(int(start), int(end) + 1):
            _list.append(i)
    return _list


# в отдельную функцию, чтобы в редакторе можно было свернуть ;)
def args_parser():
    args_parse = argparse.ArgumentParser()

    args_parse.add_argument('--folder',
                            help='папка, в которую будут сохранены решения',
                            metavar='f',
                            required=True)

    args_parse.add_argument(
        '--exclude',
        help='задание, которое нужно исключить из обработки',
        metavar='n',
        type=int,
        nargs='+')

    args_parse.add_argument(
        '--exclude-range',
        help='диапазон заданий, которые нужно исключить из обработки',
        metavar='n-n',
        nargs='+')

    args_parse.add_argument('--include',
                            help='задание, которое нужно включить в обработку',
                            metavar='n',
                            type=int,
                            nargs='+')

    args_parse.add_argument(
        '--include-range',
        help='диапазон заданий, которые нужно включить в обработку',
        metavar='n-n',
        nargs='+')

    args = args_parse.parse_args()

    exclude = []

    if args.exclude:
        exclude.extend(args.exclude)

    if args.exclude_range:
        exclude = extend_list(exclude, args.exclude_range)

    include = []

    if args.include:
        include.extend(args.include)

    if args.include_range:
        include = extend_list(include, args.include_range)

    # убираем дубликаты
    include = list(dict.fromkeys(include))

    # убираем ненужные
    for item in exclude:
        if item in include:
            include.remove(item)

    # сортируем
    # P.S. Не обязательно, можно убрать
    include.sort()

    return include, args.folder


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def initialize():
    clear()
