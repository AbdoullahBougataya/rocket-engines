import requests
from bs4 import BeautifulSoup
import re

def Wikipedia(engine_name = ""):
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
            if (string_element.find('Д') != -1 or string_element.find('Д') != -1 or string_element.find('Д') != -1) and string_element.find('/') == -1:
                string_element = string_element[:5]
            if titles[j] == 'Mass (kg)' and string_element.find('with fuel') != -1:
                titles[j] = 'Mass with fuel (kg)'
            elif titles[j] == 'Mass (kg)' or titles[j] == 'Mass with fuel (kg)':
                titles[j] = 'Mass (kg)'
            if titles[j] == 'Specific impulse (s)':
                titles[j] = 'Specific impulse Vac (s)'
                dictionary['Specific impulse SL (s)'] = ''
            if titles[j] == 'Thrust (N)':
                titles[j] = 'Thrust Vac (N)'
                dictionary['Thrust SL (N)'] = ''
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                if string_element.find('–') != -1:
                    dictionary['Specific impulse Vac (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse Vac (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Specific impulse SL (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse SL (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            elif titles[j] == 'Thrust Vac (N)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                if string_element.find('–') != -1:
                    dictionary['Thrust Vac (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Thrust Vac (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Thrust SL (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Thrust SL (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            elif string_element.replace("(SL)", "").replace("with fuel", "").replace(".", "").isnumeric():
                if string_element.find('–') != -1:
                    dictionary[titles[j]] = (float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2
                else:
                    dictionary[titles[j]] = float(string_element.replace("(SL)", "").replace("with fuel", ""))
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
            if titles[j] == 'Mass (kg)' and string_element.find('with fuel') != -1:
                titles[j] = 'Mass with fuel (kg)'
            elif titles[j] == 'Mass (kg)' or titles[j] == 'Mass with fuel (kg)':
                titles[j] = 'Mass (kg)'
            if titles[j] == 'Specific impulse (s)':
                titles[j] = 'Specific impulse Vac (s)'
                dictionary['Specific impulse SL (s)'] = ''
            if titles[j] == 'Thrust (N)':
                titles[j] = 'Thrust Vac (N)'
                dictionary['Thrust SL (N)'] = ''
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                if string_element.find('–') != -1:
                    dictionary['Specific impulse Vac (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse Vac (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Specific impulse SL (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse SL (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            elif titles[j] == 'Thrust Vac (N)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                if string_element.find('–') != -1:
                    dictionary['Thrust Vac (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Thrust Vac (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Thrust SL (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Thrust SL (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            elif string_element.replace("(SL)", "").replace("with fuel", "").replace(".", "").isnumeric():
                if string_element.find('–') != -1:
                    dictionary[titles[j]] = (float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2
                else:
                    dictionary[titles[j]] = float(string_element.replace("(SL)", "").replace("with fuel", ""))
            else:
                dictionary[titles[j]] = string_element
        if dictionary != {}:
            dictionary["Status"] = "Retired"
            dict.append(dictionary)
    engines = {}
    for i in range(len(dict) - 1):
        tmp = dict[i]
        Twomp = tmp['Engine']
        engines[Twomp] = dict[i]
    if engine_name != "":
        try:
            return engines[engine_name]
        except KeyError:
            print(f'Error: {engine_name} is not a name of an orbital rocket engine.')
            return f'Error: {engine_name} is not a name of an orbital rocket engine.'
    else:
        return engines

print(Wikipedia('AJ-10-190'))
