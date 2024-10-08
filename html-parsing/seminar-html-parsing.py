import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

url = 'https://www.boxofficemojo.com'

ua = UserAgent()  #random user agents decreases a chance to be blocked
headers = {'User-Agen': ua.random}
params = {'ref_': 'bo_nb_hm_tab'}

session = requests.session()

response = session.get(url + '/intl', params=params, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print()
# test_link = soup.find('a', {'class': 'a-link-normal'})

movies = []
rows = soup.find_all('tr')

for row in rows[2:10]:
    movie = {}

    # area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).find('a')
    try:
        area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]

    except:
        area_info = None

    movie['area'] = [
        area_info.getText(),
        url + area_info.get('href')
    ]

    weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
    movie['weekend'] = [
        weekend_info.getText(),
        url + weekend_info.get('href')
    ]

    movie['releases'] = row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText()

    frelease_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
    movie['weekend'] = [
        frelease_info.getText(),
        url + frelease_info.get('href')
    ]

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        movie['weekend'] = [
            distributor_info.getText(),
            url + distributor_info.get('href')
        ]
    except:
        print(f'Exception with frelease, object = {movie[frelease_info]}')
        distributor_info = None

    movie['gross'] = row.find('td', {'class': 'mojo-field-type-money'}).getText()

    movies.append(movie)

pprint(movies)
