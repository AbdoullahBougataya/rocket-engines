import requests
from bs4 import BeautifulSoup

research_later = "F-1"
goog_search = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + research_later.replace(" ", "+") + "+rocket+engine+wikipedia"


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
    print(soup.find_all("img")[3])
