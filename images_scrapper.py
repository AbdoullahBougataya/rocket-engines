import requests
from bs4 import BeautifulSoup
import scrapper
import os

def download_image(image_url, file_dir):
    response = requests.get(image_url)

    if response.status_code == 200:
        directory = os.path.dirname(file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_dir, "wb") as fp:
            fp.write(response.content)
        print("Image downloaded successfully.")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

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
                        pic_url = "https:" + str(soup.find("table", {"class" : "infobox"}).find("td", {"class": "infobox-image"}).find("img").get("srcset").split()[2])
                        download_image(pic_url, f"/images/{engine_name}.jpg")
