import requests
from bs4 import BeautifulSoup
import scrapper
import os, shutil
import sys

# This function download images from a given URL to a file directory
def download_image(image_url, file_dir):
    response = requests.get(image_url, headers = {'User-Agent': 'NicoBot/0.1 (your@email.address)'})

    if response.status_code == 200:
        directory = os.path.dirname(file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_dir, "wb") as fp:
            fp.write(response.content)

# Clear the images file
for filename in os.listdir("./images"):
    file_path = os.path.join("./images", filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# This function scrappes images of rocket engines
def images_scrapper():
    print("Downloading images...")
    engines = scrapper()[1]
    paths = ()
    c = 0
    for engine in engines:
        path = ""
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
                        if len(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()) > 2 and "Aeon" not in engine_name:
                            pic_url = "https:" + str(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()[2])
                            path = f"./images/{engine_name}.jpg"
                            download_image(pic_url, path)
        c += 1
        print(f"{100 * (c/len(engines))} % done")
        paths += tuple(path)
    return paths

sys.modules[__name__] = images_scrapper
