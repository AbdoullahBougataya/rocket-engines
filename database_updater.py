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
    table += f"""'{titles[i]}'"""
    if type(engines[7][i]) == str:
        table += """ TEXT, """
    elif type(engines[7][i]) == float:
        table += """ REAL, """
table = table.removesuffix(""", """)
table += """); """
cur.execute(table)

print("Table is Ready")

for i in range(len(engines)):
    print(f"""INSERT INTO ENGINES VALUES {engines[i]};""".replace("''", "NULL"))
    cur.execute(f"""INSERT INTO ENGINES VALUES {engines[i]};""".replace("''", "NULL"))
print("Table successfully filled")
# Close the connection
con.close()
