import requests
from bs4 import BeautifulSoup

html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
soup = BeautifulSoup(html.text, 'html.parser')
table = soup.find_all('table')[0]
rows = table.find_all('tr')
for row in range(len(rows) - 1):
    print(rows[row + 1])
