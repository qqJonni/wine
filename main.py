from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas
import pprint
from collections import defaultdict


data = pandas.read_excel('wine2.xlsx')

result = defaultdict(list)

for _, row in data.iterrows():
    category = row['Категория']
    product = {
        'Название': row['Название'],
        'Сорт': row['Сорт'],
        'Цена': row['Цена'],
        'Картинка': row['Картинка']
    }
    result[category].append(product)

result = dict(result)

pprint.pprint(result)


excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1', usecols=['Название', 'Сорт', 'Цена', 'Картинка'])


def format_years(number):
    if number % 100 in [11, 12, 13, 14]:
        return f"{number} лет"

    last_digit = number % 10

    if last_digit == 1:
        return f"{number} год"
    elif last_digit in [2, 3, 4]:
        return f"{number} года"
    else:
        return f"{number} лет"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')
past_date = datetime(1920, 4, 10)
current_date = datetime.now()
time_difference = current_date - past_date
years_difference = time_difference.days // 365

wines = []
for i in range(len(excel_data_df)):
    wine = {
        'title': excel_data_df['Название'][i],
        'sort': excel_data_df['Сорт'][i],
        'price': excel_data_df['Цена'][i],
        'image': excel_data_df['Картинка'][i]
    }
    wines.append(wine)

rendered_page = template.render(wines=wines, years_old=f'Мы уже {format_years(years_difference)} с вами')

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()