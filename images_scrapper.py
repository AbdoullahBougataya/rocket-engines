import requests
from bs4 import BeautifulSoup
import scrapper
import time

titles, engines = scrapper()
for engine in engines:
    engine_name = engine[0]
    goog_search = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + engine_name.replace(" ", "+") + "+rocket+engine+wikipedia"


    r = requests.get(goog_search)

    soup = BeautifulSoup(r.text, "html.parser")
    search_result = soup.find_all("a")
    for i in range(len(search_result)):
        if "https://en.wikipedia.org/wiki/" in str(search_result[i]):
            the_link = search_result[i]
            break
    if the_link:
        wikipedia_link = str(the_link.get('href')).removeprefix("/url?q=").split("&")[0]
        r = requests.get(wikipedia_link)
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.find("table", {"class" : "infobox"}):
            if soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}):
                if soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset"):
                    if len(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()) > 2:
                        print("https:" + str(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()[2]))
                        pic_url = "https:" + str(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()[2])
                        with open(f'images/{engine_name}.jpg', 'wb') as handler:
                            response = requests.get(pic_url, stream=True)
                            for block in response.iter_content(1024):
                                if not block:
                                    break
                                handler.write(block)
                        time.sleep(3)
