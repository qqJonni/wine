from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas
from collections import defaultdict
import argparse


def get_name_year(number):
    if number % 100 in [11, 12, 13, 14]:
        return f"{number} лет"

    last_digit = number % 10

    if last_digit == 1:
        return f"{number} год"
    elif last_digit in [2, 3, 4]:
        return f"{number} года"
    else:
        return f"{number} лет"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate website from wine Excel data.')
    parser.add_argument('filename', help='The Excel filename')
    args = parser.parse_args()

    table = pandas.read_excel(args.filename)
    dictionary_object = defaultdict(list)

    for _, row in table.iterrows():
        category = row['Категория']
        product = {
            'Название': row['Название'],
            'Сорт': row['Сорт'],
            'Цена': row['Цена'],
            'Картинка': row['Картинка']
        }
        dictionary_object[category].append(product)

    wine_dictionary = dict(dictionary_object)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    past_date = datetime(1920, 4, 10)
    current_date = datetime.now()

    years_difference = current_date.year - past_date.year

    rendered_page = template.render(years_old=f'Мы уже {get_name_year(years_difference)} с вами', result=wine_dictionary)

    with open('template.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

