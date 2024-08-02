import requests
from bs4 import BeautifulSoup

research_later = "F-1"
goog_search = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + research_later.replace(" ", "+") + "+rocket+engine+wikipedia"


r = requests.get(goog_search)

soup = BeautifulSoup(r.text, "html.parser")
search_result = soup.find_all("a", {"data-ved" : "2ahUKEwj21_Cf_daHAxVL1zgGHWfiDjAQFnoECAsQAg"})
print(search_result)
