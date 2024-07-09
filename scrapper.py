import requests

html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines')
print(html.text)
