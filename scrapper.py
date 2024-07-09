import wikipedia

section = wikipedia.WikipediaPage('Comparison of orbital rocket engines').section('Current, Upcoming, and In-Development rocket engines')

section = section.replace('\n', '').replace("\'", "")
print(section)
