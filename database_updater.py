import sqlite3
import scrapper

con = sqlite3.connect('db\database.db')

# cursor object
cur = con.cursor()

# Drop the GEEK table if already exists.
cur.execute("DROP TABLE IF EXISTS ENGINES")

titles, engines = scrapper()

# Creating table
table = """ CREATE TABLE ENGINES (Id INTEGER NOT NULL, """
for i in range(len(titles)):
    table += titles[i]
    if typeof(engines[7][i]) == str:
        table += """ TEXT, """
    elif typeof(engines[7][i]) == float:
        table += """ REAL, """

            Engine TEXT NOT NULL,
            Origin TEXT NOT NULL,
            Designer TEXT,
            Vehicle TEXT,
            Status TEXT NOT NULL,
            Use TEXT,
            Propellant TEXT,
            'Power cycle' TEXT,
            'Specific impulse Vac (s)' REAL,
            'Specific impulse SL (s)' REAL,
            'Thrust Vac (N)' REAL,
            'Thrust SL (N)' REAL,
            'Chamber pressure (bar)' REAL,
            'Mass (kg)' TEXT,
            'Thrust weight ratio' REAL,
            'Oxidiser:fuel ratio' REAL
        ); """

cur.execute(table)

print("Table is Ready")

# Close the connection
con.close()
