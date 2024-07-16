import sqlite3
import scrapper

con = sqlite3.connect('db\database.db')

# cursor object
cur = con.cursor()

# Drop the GEEK table if already exists.
cur.execute("DROP TABLE IF EXISTS ENGINES")

engines = scrapper()

# Creating table
table = """ CREATE TABLE ENGINES (
            Id INTEGER NOT NULL,
            Engine TEXT NOT NULL,
            Origin TEXT NOT NULL,
            Designer TEXT,
            Vehicle TEXT,
            Status TEXT NOT NULL,
            Use TEXT,
            Propellant TEXT,
            'Power cycle' TEXT,
            'Specific impulse (s)' REAL,
            'Thrust (N)' REAL,
            'Chamber pressure (bar)' REAL,
            'Mass (kg)' TEXT,
            'Thrust weight ratio' REAL,
            'Oxidiser:fuel ratio' REAL
        ); """

cur.execute(table)

for i in range(len(engines)):
    query = f"""INSERT INTO ENGINES (Id, Engine, Origin, Designer, Vehicle, Status, Use, Propellant, 'Power cycle', 'Specific impulse (s)', 'Thrust (N)', 'Chamber pressure (bar)', 'Mass (kg)', 'Thrust weight ratio', 'Oxidiser:fuel ratio') VALUES({i}"""
    for element in engines[i]:
        query += f", {engines[i][element]}"
    query += """);"""
    print(query)
    cur.execute(query)

print("Table is Ready")

# Close the connection
con.close()
