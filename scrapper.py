import requests
from bs4 import BeautifulSoup

html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
soup = BeautifulSoup(html.text, 'html.parser')
print(soup.table.prettify())
