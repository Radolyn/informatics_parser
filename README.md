# Informatics parser

Универсальный парсер задач с informatics.mccme.ru (informatics.msk.ru)

## Использование

```help
usage: parser.py [-h] --folder f [--range n-n] [--one n] [--exclude n [n ...]] [--exclude-range n-n [n-n ...]] [--include n [n ...]]
                 [--include-range n-n [n-n ...]]

optional arguments:
  -h, --help            show this help message and exit
  --folder f            папка, в которую будут сохранены решения
  --range n-n           диапазон заданий, который нужно обработать
  --one n               задание, которое нужно обработать
  --exclude n [n ...]   задание, которое нужно исключить из обработки
  --exclude-range n-n [n-n ...]
                        диапазон заданий, которые нужно исключить из обработки
  --include n [n ...]   задание, которое нужно включить в обработку
  --include-range n-n [n-n ...]
                        диапазон заданий, которые нужно включить в обработку
```

## Участие

Если у вас есть идеи по улучшению парсера - можете создать pull request или issue.
