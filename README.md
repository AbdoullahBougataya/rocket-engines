# Rocket Engines API
 > [!WARNING]
 > The data scrapped to the database have been modified several times throughout the code, so keep in mind that the data is a bare approximate and doesn't always reflect real world circumstances.
## Introduction
One day an idea came to my mind to create a game that simulate rocket development using real world rocket physics. So naturally a started searching for an API that stores data about orbital rocket engines. I found many APIs related to space launch systems but I was not able to find a proper API that stores in informations about rocket engines. Due to the hard nature of creating a game that simulate rocket development and my limited knowledge in game development I decided to cancel that project and rather decided to focus on making an API that stores orbital rocket engines informations.
## Walkthrough
* The file `scrapper.py` returns a function called scrapper(), this is function is the function that scrappes the net (Wikipedia in this example) for data about the orbitale rocket engines.
* `database_updater.py` is the python program that updates the database.
* In the folder `db` there is a file called `database.db`, this file contains the database of orbital rocket engines.
