import requests
from bs4 import BeautifulSoup
import re
import sys

# scrapper() is a function that scrape the elements of the list that contains the informations about rocket engines. This function return a dictionary that contains those elements.
def scrapper():
    # get the html from scrapper
    link = 'https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines'
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    # get and format the first table (contain new rocket engines) titles from html
    titles_bs = soup.find_all('table')[0].find_all('th')
    titles = ()
    for i in range(len(titles_bs)):
        title = re.sub("\[.*?\]","[]",titles_bs[i].get_text().replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", "")
        if title == 'Specific impulse (s)':
            titles += tuple(map(str, ['Specific impulse Vac (s)']))
            titles += tuple(map(str, ['Specific impulse SL (s)']))
        elif title == 'Thrust (N)':
            titles += tuple(map(str, ['Thrust Vac (N)']))
            titles += tuple(map(str, ['Thrust SL (N)']))
        else:
            titles += tuple(map(str, [title]))
    # get the table rows
    rows_bs = soup.find_all('table')[0].find_all('tr')
    dict = []
    for i in range(len(rows_bs)):
        # find all the elements from every row
        element = rows_bs[i].find_all('td')
        row = ()
        for j in range(len(element)):
            # define the string_element as a cell from the table [It will get every element as string even if it's a number]
            string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").replace("est.", "").replace("~", "").replace(">", "").replace("<", "").removesuffix("\n")
            # Clean the titles and the strings from unwanted elements
            if string_element.find('Д') != -1:
                string_element = string_element.split()[0]
            # Split the specific impulse column into Isp in the vaccum and Isp in the sea level
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change the Isp in the vaccum intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2, (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0]), float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])]))
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            elif titles[j] == 'Specific impulse SL (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change Thrust in the vaccum intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2, (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0]), float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])]))
            # Change numbers from strings to floats
            elif string_element.replace("(SL)", "").strip().replace("–", "").replace(".", "").isnumeric() and titles[j] != 'Thrust SL (N)':
                # Change intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(string_element.replace("(SL)", "").replace("with fuel", ""))]))
                if titles[j] == 'Specific impulse Vac (s)' or titles[j] == 'Specific impulse SL (s)':
                    row += tuple(map(str, [""]))
            else:
                # assigning the string element from the table to a value in the dictionary
                row += tuple(map(str, [string_element]))
                if titles[j] == 'Specific impulse Vac (s)' or titles[j] == 'Specific impulse SL (s)':
                    row += tuple(map(str, [""]))
        # append the list dict with the dictionary if it is not empty
        if row != ():
            dict.append(row)
    # get the table rows
    titles_bs = soup.find_all('table')[0].find_all('th')
    titlesr = ()
    for i in range(len(titles_bs)):
        title = re.sub("\[.*?\]","[]",titles_bs[i].get_text().replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", "")
        if title == 'Specific impulse (s)':
            titlesr += tuple(map(str, ['Specific impulse Vac (s)']))
            titlesr += tuple(map(str, ['Specific impulse SL (s)']))
        elif title == 'Thrust (N)':
            titlesr += tuple(map(str, ['Thrust Vac (N)']))
            titlesr += tuple(map(str, ['Thrust SL (N)']))
        else:
            titlesr += tuple(map(str, [title]))
    rows_bs = soup.find_all('table')[1].find_all('tr')
    for i in range(len(rows_bs)):
        # find all the elements from every row
        element = rows_bs[i].find_all('td')
        row = ()
        for j in range(len(element)):
            # define the string_element as a cell from the table [It will get every element as string even if it's a number]
            string_element = re.sub("\[.*?\]","[]", element[j].get_text().replace("\u200b", "").replace("\u2009", "").replace("\xa0", "").replace("  ", " ")).replace("[]", "").replace(",", "").replace("est.", "").replace("~", "").replace(">", "").replace("<", "").removesuffix("\n")
            # Clean the titles and the strings from unwanted elements
            if string_element.find('Д') != -1:
                string_element = string_element.split()[0]
            # Split the specific impulse column into Isp in the vaccum and Isp in the sea level
            if titlesr[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change the Isp in the vaccum intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2, (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0]), float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])]))
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            elif titlesr[j] == 'Specific impulse SL (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change Thrust in the vaccum intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2, (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0]), float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])]))
            # Change numbers from strings to floats
            elif string_element.replace("(SL)", "").strip().replace("–", "").replace(".", "").isnumeric() and titlesr[j] != 'Thrust Vac (N)':
                # Change intervals to median
                if string_element.find('–') != -1:
                    row += tuple(map(float, [(float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2]))
                else:
                    row += tuple(map(float, [float(string_element.replace("(SL)", "").replace("with fuel", ""))]))
                if titlesr[j] == 'Specific impulse Vac (s)' or titlesr[j] == 'Specific impulse SL (s)':
                    row += tuple(map(str, [""]))
            else:
                # assigning the string element from the table to a value in the dictionary
                row += tuple(map(str, [string_element]))
                if titlesr[j] == 'Specific impulse Vac (s)' or titlesr[j] == 'Specific impulse SL (s)':
                    row += tuple(map(str, [""]))
        # append the list dict with the dictionary if it is not empty
        if row != ():
            if row[0] == 'P230':
                row += ('', )
            row = list(row)
            row.insert(4, "Retired")
            dict.append(tuple(row))
    # Handle the function parameter
    return titles, dict

sys.modules[__name__] = scrapper
