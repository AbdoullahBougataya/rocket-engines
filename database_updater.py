import sqlite3
import scrapper

con = sqlite3.connect('db\database.db')

# cursor object
cur = con.cursor()

# Drop the rocket_engines table if already exists.
cur.execute("DROP TABLE IF EXISTS rocket_engines")

titles, engines = scrapper()

# Creating table
table = """ CREATE TABLE rocket_engines (Id INTEGER NOT NULL PRIMARY KEY, """
for i in range(len(titles)):
    table += f"""'{titles[i]}'"""
    if type(engines[17][i]) == str:
        table += """ TEXT, """
    elif type(engines[17][i]) == float:
        table += """ REAL, """
table = table.removesuffix(""", """)
table += """); """
cur.execute(table)

print("Table is Ready")

for i in range(len(engines)):
    cur = con.cursor()
    cur.execute("INSERT INTO rocket_engines ? VALUES ?;".replace("''", "NULL"), titles, engines[i])
    con.commit()

print("Table successfully filled")
# Close the connection
con.close()
