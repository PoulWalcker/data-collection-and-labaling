import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import json

url = 'https://books.toscrape.com/'

ua = UserAgent()
headers = {'User-Agen': ua.random}
session = requests.session()
page = 1

all_books_data = []

while True:

    response = session.get(url + f'/catalogue/page-{page}.html', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', {'class': 'product_pod'})

    if not books:
        break

    print(f'Page #{page} in process...')

    for book in books:
        book_info = {}
        book_title = book.find('h3').findChildren()[0]
        book_link = book_title.get('href')

        try:
            inner_response = session.get(url + f'catalogue/' + book_link, headers=headers)
            soup = BeautifulSoup(inner_response.text, 'html.parser')
            inner_page = soup.find('article', {'class': 'product_page'})
            stock_data = inner_page.find('p', {'class': 'instock availability'})

            if stock_data:
                stock_amount = int(re.search(r'\d+', stock_data.getText()).group())
                book_info['stock_amount'] = stock_amount
            else:
                book_info['stock_amount'] = 0

            p_tags = inner_page.find_all('p')

            if len(p_tags) <= 3:
                book_info['desc'] = None
            else:
                book_info['desc'] = p_tags[3].getText()

        except Exception as e:
            print(f'Error: {e}')
            book_info['stock_amount'] = 0

        book_info['title'] = book_title.get('title')
        book_info['price'] = float(re.search(r'\d+\.\d+', book.find('p', {'class': 'price_color'}).getText()).group())
        all_books_data.append(book_info)
    page += 1

json_data = json.dumps(all_books_data)

with open("book_store_data.json", "w") as file:
    file.write(json_data)
