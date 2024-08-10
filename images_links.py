import requests
from bs4 import BeautifulSoup
import scrapper
import sys

# This function get the links of images of rocket engines
def images_links():
    engines = scrapper()[1]
    print("Getting images links...")
    paths = ()
    wikipedia_pages = {}
    c = 0
    for engine in engines:
        pic_url = ""
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
            wikipedia_pages[engine_name] = wikipedia_link
            r = requests.get(wikipedia_link)
            soup = BeautifulSoup(r.text, "html.parser")
            if soup.find("table", {"class" : "infobox"}):
                if soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}):
                    if soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset"):
                        if len(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()) > 2 and "Aeon" not in engine_name:
                            pic_url = "https:" + str(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()[2])
        c += 1
        print(f"{int(100 * (c/len(engines)))}% done")
        paths += (pic_url, )
    print(f"100% done")
    return paths, wikipedia_pages

sys.modules[__name__] = images_links
