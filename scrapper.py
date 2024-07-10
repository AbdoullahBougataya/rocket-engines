import requests
from bs4 import BeautifulSoup
import re

html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
soup = BeautifulSoup(html.text, 'html.parser')
titles_bs = soup.find_all('table')[0].find_all('th')
titles = []
for i in range(len(titles_bs)):
    title = titles_bs[i].get_text()
    titles.append(re.sub("\[.*?\]","[]",title.replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", ""))
rows_bs = soup.find_all('table')[0].find_all('tr')
dict = []
for i in range(len(rows_bs)):
    element = rows_bs[i].find_all('td')
    dictionary = {}
    for j in range(len(element)):
        string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").removesuffix("\n")
        if string_element.replace(".", "").isnumeric():
            dictionary[titles[j]] = float(string_element)
        else:
            dictionary[titles[j]] = string_element
    if dictionary != {}:
        dict.append(dictionary)
titles_bs = soup.find_all('table')[1].find_all('th')
titles = []
for i in range(len(titles_bs)):
    title = titles_bs[i].get_text()
    titles.append(re.sub("\[.*?\]","[]",title.replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", ""))
rows_bs = soup.find_all('table')[1].find_all('tr')
for i in range(len(rows_bs)):
    element = rows_bs[i].find_all('td')
    dictionary = {}
    for j in range(len(element)):
        string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").removesuffix("\n")
        if string_element.replace(".", "").isnumeric():
            dictionary[titles[j]] = float(string_element)
        else:
            dictionary[titles[j]] = string_element
    dictionary["Status"] = "Retired"
    if len(dictionary['Specific impulse (s)'].split()) > 1:
        
    if dictionary != {}:
        dict.append(dictionary)
print(dict[11]['Specific impulse (s)'])
