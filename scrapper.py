import requests
from bs4 import BeautifulSoup
import re

def Wikipedia(engine_name = ""):
    # get the html from Wikipedia
    html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
    soup = BeautifulSoup(html.text, 'html.parser')
    # get and format the table titles from html
    titles_bs = soup.find_all('table')[0].find_all('th')
    titles = []
    for i in range(len(titles_bs)):
        title = titles_bs[i].get_text()
        titles.append(re.sub("\[.*?\]","[]",title.replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", ""))
    # get the table rows
    rows_bs = soup.find_all('table')[0].find_all('tr')
    dict = []
    for i in range(len(rows_bs)):
        # find all the elements from every row
        element = rows_bs[i].find_all('td')
        dictionary = {}
        for j in range(len(element)):
            # define the string_element as a cell from the table [It will get every element as string even if it's a number]
            string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").replace("est.", "").replace("~", "").replace(">", "").replace("<", "").removesuffix("\n")
            # Clean the titles and the strings from unwanted elements
            if string_element.find('Д') != -1:
                string_element = string_element.split()[0]
            if titles[j] == 'Mass (kg)' and string_element.find('with fuel') != -1:
                titles[j] = 'Mass with fuel (kg)'
                string_element = string_element.replace('with fuel', '')
            elif titles[j] == 'Mass (kg)' or titles[j] == 'Mass with fuel (kg)':
                titles[j] = 'Mass (kg)'
            # Split the specific impulse column into ISP in the vaccum and ISP in the sea level
            if titles[j] == 'Specific impulse (s)':
                titles[j] = 'Specific impulse Vac (s)'
                dictionary['Specific impulse SL (s)'] = ''
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            if titles[j] == 'Thrust (N)':
                titles[j] = 'Thrust Vac (N)'
                dictionary['Thrust SL (N)'] = ''
            # Split the specific impulse column into ISP in the vaccum and ISP in the sea level
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                if string_element.find('–') != -1:
                    dictionary['Specific impulse Vac (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse Vac (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Specific impulse SL (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse SL (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            elif titles[j] == 'Thrust Vac (N)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change Thrust in the vaccum intervals to median
                if string_element.find('–') != -1:
                    dictionary['Thrust Vac (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Thrust Vac (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                if string_element.find('–') != -1:
                    dictionary['Thrust SL (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Thrust SL (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            # Change numbers from strings to floats
            elif string_element.replace("(SL)", "").strip().replace("–", "").replace("with fuel", "").replace(".", "").isnumeric():
                # Change intervals to median
                if string_element.find('–') != -1:
                    dictionary[titles[j]] = (float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2
                else:
                    dictionary[titles[j]] = float(string_element.replace("(SL)", "").replace("with fuel", ""))
            else:
                # assigning the string element from the table to a value in the dictionary
                dictionary[titles[j]] = string_element
        # append the list dict with the dictionary if it is not empty
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
            if string_element.find('Д') != -1 or string_element.find('11D') != -1 or string_element.find('15D') != -1 or string_element.find('8D') != -1:
                string_element = string_element.split()[0]
            if titles[j] == 'Mass (kg)' and string_element.find('with fuel') != -1:
                titles[j] = 'Mass with fuel (kg)'
                string_element = string_element.replace('with fuel', '')
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
            elif string_element.replace("(SL)", "").strip().replace("with fuel", "").replace("–", "").replace(".", "").isnumeric():
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
    for i in range(len(dict)):
        engines[dict[i]['Engine']] = dict[i]
    if engine_name != "":
        try:
            return engines[engine_name]
        except KeyError:
            print(f'Error: {engine_name} is not a name of an orbital rocket engine.')
            return f'Error: {engine_name} is not a name of an orbital rocket engine.'
    else:
        return engines

print(Wikipedia(''))
