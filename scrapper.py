import requests
from bs4 import BeautifulSoup
import re
import sqlite3

# scrapper() is a function that scrape the elements of the list that contains the informations about rocket engines. This function return a dictionary that contains those elements.
def scrapper():
    # get the html from scrapper
    html = requests.get('https://en.scrapper.org/wiki/Comparison_of_orbital_rocket_engines')
    soup = BeautifulSoup(html.text, 'html.parser')
    # get and format the first table (contain new rocket engines) titles from html
    titles_bs = soup.find_all('table')[0].find_all('th')
    titles = []
    datatypes = ['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'REAL', 'REAL', 'REAL', 'TEXT', 'REAL', 'REAL']
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
            # Split the specific impulse column into ISP in the vaccum and ISP in the sea level
            if titles[j] == 'Specific impulse (s)':
                titles[j] = 'Specific impulse Vac (s)'
                dictionary['Specific impulse SL (s)'] = ''
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            if titles[j] == 'Thrust (N)':
                titles[j] = 'Thrust Vac (N)'
                dictionary['Thrust SL (N)'] = ''
            # Split the specific impulse column into Isp in the vaccum and Isp in the sea level
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change the Isp in the vaccum intervals to median
                if string_element.find('–') != -1:
                    dictionary['Specific impulse Vac (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse Vac (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                # Change the Isp in the surface level intervals to median
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
                # Change Thrust in the surface level intervals to median
                if string_element.find('–') != -1:
                    dictionary['Thrust SL (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Thrust SL (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            # Change numbers from strings to floats
            elif string_element.replace("(SL)", "").strip().replace("–", "").replace("with fuel", "").replace(".", "").isnumeric() and titles[j] != 'Mass (kg)':
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
    # get and format the second table (contain old rocket engines) titles from html
    titles_bs = soup.find_all('table')[1].find_all('th')
    titles = []
    for i in range(len(titles_bs)):
        title = titles_bs[i].get_text()
        titles.append(re.sub("\[.*?\]","[]",title.replace("\n", "").replace("\u200b", "").replace("  ", " ")).replace("[]", ""))
    # get the table rows
    rows_bs = soup.find_all('table')[1].find_all('tr')
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
            # Split the specific impulse column into ISP in the vaccum and ISP in the sea level
            if titles[j] == 'Specific impulse (s)':
                titles[j] = 'Specific impulse Vac (s)'
                dictionary['Specific impulse SL (s)'] = ''
            # Split the thrust column into Thrust in the vaccum and Thrust in the sea level
            if titles[j] == 'Thrust (N)':
                titles[j] = 'Thrust Vac (N)'
                dictionary['Thrust SL (N)'] = ''
            # Split the specific impulse column into Isp in the vaccum and Isp in the sea level
            if titles[j] == 'Specific impulse Vac (s)' and len(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()) > 1:
                # Change the Isp in the vaccum intervals to median
                if string_element.find('–') != -1:
                    dictionary['Specific impulse Vac (s)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0].split('–')[1])) / 2
                else:
                    dictionary['Specific impulse Vac (s)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[0])
                # Change the Isp in the surface level intervals to median
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
                # Change Thrust in the surface level intervals to median
                if string_element.find('–') != -1:
                    dictionary['Thrust SL (N)'] = (float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[0]) + float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1].split('–')[1])) / 2
                else:
                    dictionary['Thrust SL (N)'] = float(re.sub("\(.*?\)","()", string_element).replace("()", "").replace("  ", " ").split()[1])
            # Change numbers from strings to floats
            elif string_element.replace("(SL)", "").strip().replace("–", "").replace("with fuel", "").replace(".", "").isnumeric() and titles[j] != 'Mass (kg)':
                # Change intervals to median
                if string_element.find('–') != -1:
                    dictionary[titles[j]] = (float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[0]) + float(string_element.replace("(SL)", "").replace("with fuel", "").split('–')[1])) / 2
                else:
                    dictionary[titles[j]] = float(string_element.replace("(SL)", "").replace("with fuel", ""))
            else:
                # Assigning the string element from the table to a value in the dictionary
                dictionary[titles[j]] = string_element
        # Append the list dict with the dictionary and add an status of retired if it is not empty
        if dictionary != {}:
            dictionary["Status"] = "Retired"
            dict.append(dictionary)
    # Handle the function parameter
    return dict, titles, datatypes

try:
	# Making a connection between sqlite3 database and Python Program
	con = sqlite3.connect('db\database.db')
	# If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
	# Otherwise it will show errors
	print("Connected to SQLite")
except sqlite3.Error as error:
	print("Failed to connect with the sqlite3 database", error)
finally:
	# Inside Finally Block, If connection is open
	if con:
		cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS engines")
		cur.execute("CREATE TABLE engines (id INT)")
		engines, titles, datatype = scrapper()
		for i in titles:
		    cur.execute(f"ALTER TABLE engines ADD '{i}' {datatype}")
		cur.execute("SELECT * FROM engines")
		# using close() method, we will close the connection
		con.close()
		# After closing connection object, we will print "the sqlite connection is closed"
		print("the sqlite connection is closed")
