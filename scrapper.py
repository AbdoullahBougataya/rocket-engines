import requests
from bs4 import BeautifulSoup
import re

html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
soup = BeautifulSoup(html.text, 'html.parser')
titles_bs = soup.find_all('th')
titles = []
for i in range(len(titles_bs)):
    title = titles_bs[i].get_text()
    titles.append(re.sub("\[.*?\]","[]",title.replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", ""))
rows_bs = soup.find_all('table')[0].find_all('tr')
rows = []
for i in range(len(rows_bs)):
    element = rows_bs[i].find_all('td')
    dictionary = {}
    for j in range(len(element)):
        dictionary[titles[j]] = re.sub("\[.*?\]","[]", element[j].get_text().replace("\n", "").replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "")
    rows.append(dictionary)
print(rows)
