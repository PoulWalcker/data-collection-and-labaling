import os
from dotenv import load_dotenv
import requests

if load_dotenv():
    print(".env file is successfully downloaded")
else:
    print(".env is not found")

api_key = os.getenv('API_KEY')

url = "https://api.foursquare.com/v3/places/search"
headers = {"accept": "application/json",
           "Authorization": api_key}

prompt = '''Choose the desired category:
1. Coffee
2. Museum
3. Parks
'''

categories = {
    1: 'coffee',
    2: 'museum',
    3: 'parks'
}

category_index = int(input(prompt))

response = requests.get(f'url{categories[category_index]}', headers=headers)

print('Results:')
print('')
