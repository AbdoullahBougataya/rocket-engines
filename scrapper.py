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
        string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").replace("est.", "").replace("~", "").replace(">", "").replace("<", "").removesuffix("\n")
        if titles[j] == 'Specific impulse (s)':
            titles[j] = 'Specific impulse (s) Vac'
            dictionary['Specific impulse (s) SL'] = ''
        if titles[j] == 'Thrust (N)':
            titles[j] = 'Thrust (N) Vac'
            dictionary['Thrust (N) SL'] = ''
        if titles[j] == 'Specific impulse (s) Vac' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
            dictionary['Specific impulse (s) Vac'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
            dictionary['Specific impulse (s) SL'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
        elif titles[j] == 'Thrust (N) Vac' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
            dictionary['Thrust (N) Vac'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
            dictionary['Thrust (N) SL'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
        elif string_element.replace(".", "").isnumeric():
            if string_element.find('–') != -1:
                dictionary[titles[j]] = (float(string_element.split('–')[0]) + float(string_element.split('–')[1])) / 2
            else:
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
        string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").replace("est.", "").replace("~", "").replace(">", "").replace("<", "").removesuffix("\n")
        if titles[j] == 'Specific impulse (s)':
            titles[j] = 'Specific impulse (s) Vac'
            dictionary['Specific impulse (s) SL'] = ''
        if titles[j] == 'Thrust (N)':
            titles[j] = 'Thrust (N) Vac'
            dictionary['Thrust (N) SL'] = ''
        if titles[j] == 'Specific impulse (s) Vac' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
            dictionary['Specific impulse (s) Vac'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
            dictionary['Specific impulse (s) SL'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
        elif titles[j] == 'Thrust (N) Vac' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1: # re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0]
            dictionary['Thrust (N) Vac'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
            dictionary['Thrust (N) SL'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
        elif string_element.replace(".", "").isnumeric():
            if string_element.find('–') != -1:
                dictionary[titles[j]] = (float(string_element.split('–')[0]) + float(string_element.split('–')[1])) / 2
            else:
                dictionary[titles[j]] = float(string_element)
        else:
            dictionary[titles[j]] = string_element
    dictionary["Status"] = "Retired"
    if dictionary != {}:
        dict.append(dictionary)
print(dict)
