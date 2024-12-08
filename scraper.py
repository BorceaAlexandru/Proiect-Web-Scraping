#scraper

import requests
from bs4 import BeautifulSoup

def get_game_data(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')

    print(soup)
