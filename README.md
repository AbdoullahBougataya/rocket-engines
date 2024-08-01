# Rocket Engines API 🚀

> [!WARNING]
> The data scrapped to the database have been modified several times throughout the code, so keep in mind that the data is a bare approximate and doesn't always reflect real world circumstances.
## Introduction
One day an idea came to my mind to create a game that simulate rocket development using real world rocket physics. So naturally a started searching for an API that stores data about orbital rocket engines. I found many [APIs](https://github.com/r-spacex/SpaceX-API) related to space launch systems but I was not able to find a proper API that stores in informations about rocket engines. Due to the hard nature of creating a game that simulate rocket development and my limited knowledge in game development I decided to cancel that project and rather decided to focus on making an **API that stores orbital rocket engines** informations.

## Usage

To start serving this API, you should first install [GO](https://go.dev/dl/), then change directory to `/API`. Then run: `go get github.com/mattn/go-sqlite3` after it finishes installing. run the command `go run main.go`. If everything is alright it should show `Server is running on port 8080` after asking you for permition. Make a get request to `http://localhost:8080/engines` to get started.

## Walkthrough
> The data scrapping and the database updating is made using [python](https://www.python.org/)
* The file `scrapper.py` returns a function called `scrapper()`, this is the function that scrappes the net (Wikipedia in this example) for data about the orbitale rocket engines.
* `database_updater.py` is the python program that updates the database.
* In the folder `db` there is a file called `database.db`, this file contains the database of orbital rocket engines.

> The API is made using [GOlang](https://www.go.dev/)
* The file `API/main.go` fetch the data from the database in `db/database.db` and serve it in JSON format as a Restful API
    * The API runs on port 8080.
    * Currently the API have only one endpoint `/engines`.
    * The API supports two parameters:
        * The `id` parameter, should be given the number used to identify the engine in the database.
        * The `engine` parameter, should be given the name of the of the rocket engine.
## Usage
First you will have to install [GO](https://go.dev/):
### Windows
You can download 

Legal note: scrapping Wikipedia is completely legal.

This project was made to serve as a final project for CS50.
