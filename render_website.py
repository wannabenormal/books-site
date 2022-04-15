import json
import os

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open('books.json', 'r', encoding='utf-8') as json_file:
        books = json.load(json_file)

    books_py_pages = list(chunked(books, 20))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    os.makedirs('pages', exist_ok=True)

    for page_num, page_books in enumerate(books_py_pages, 1):
        rendered_page = template.render(
            books=page_books
        )

        with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
