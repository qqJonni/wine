from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime


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
rendered_page = template.render(
    years_old=f'Мы уже {format_years(years_difference)} с вами',
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()