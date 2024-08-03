import sqlite3
import scrapper
import images_scrapper

con = sqlite3.connect('db\database.db')

# cursor object
cur = con.cursor()

# Drop the rocket_engines table if already exists.
cur.execute("DROP TABLE IF EXISTS rocket_engines")

titles, engines = scrapper()

images = images_scrapper()

# Creating table
table = """ CREATE TABLE rocket_engines (Id INTEGER NOT NULL PRIMARY KEY, """
for i in range(len(titles)):
    table += f"""'{titles[i]}'"""
    if type(engines[17][i]) == str:
        table += """ TEXT, """
    elif type(engines[17][i]) == float:
        table += """ REAL, """
table = table.removesuffix(""", """)
table += """, Image TEXT); """
cur.execute(table)

print("Table is Ready")
print("Filling the database...")
for i in range(len(engines)):
    cur = con.cursor()
    cur.execute(f"INSERT INTO rocket_engines VALUES {(i, ) + engines[i] + (images[i], )};".replace("''", "NULL"))
    con.commit()
    print(f"{int(100 * (i/len(engines)))}% done")
print(f'100% done')
print("Table successfully filled")
# Close the connection
con.close()
