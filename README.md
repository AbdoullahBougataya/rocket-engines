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
1. You can download installer GO using the link [here](https://go.dev/dl/).
2. Open the MSI file you downloaded and follow the prompts to install Go.
By default, the installer will install Go to Program Files or Program Files (x86). You can change the location as needed. After installing, you will need to close and reopen any open command prompts so that changes to the environment made by the installer are reflected at the command prompt.
### MacOS
1. You can download installer GO using the link [here](https://go.dev/dl/).
2. Open the package file you downloaded and follow the prompts to install Go.
The package installs the Go distribution to /usr/local/go. The package should put the /usr/local/go/bin directory in your PATH environment variable. You may need to restart any open Terminal sessions for the change to take effect.
### Linux
1. **Remove any previous Go installation** by deleting the /usr/local/go folder (if it exists), then extract the archive you just downloaded into /usr/local, creating a fresh Go tree in /usr/local/go:
`$ rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz`

(You may need to run the command as root or through sudo).

**Do not** untar the archive into an existing /usr/local/go tree. This is known to produce broken Go installations.
2. Add /usr/local/go/bin to the PATH environment variable.
You can do this by adding the following line to your $HOME/.profile or /etc/profile (for a system-wide installation):

`export PATH=$PATH:/usr/local/go/bin`

**Note:** Changes made to a profile file may not apply until the next time you log into your computer. To apply the changes immediately, just run the shell commands directly or execute them from the profile using a command such as source $HOME/.profile.

### How to run it

First you will have to open the terminal in the projects directory, then change the directory to API using the `cd ./API` command. After that, execute the GOlang file `main.go` using the command `go run main.go`, if you get an error telling that a package is required or missing then run `go get github.com/mattn/go-sqlite3`. If everything runs smoothly you should get a message `Server is running on port 8080`, It may ask you for permission so make sure you press allow.

Legal note: scrapping Wikipedia is completely legal.

This project was made to serve as a final project for CS50.
