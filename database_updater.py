import sqlite3

# filename to form database
file = "db\database.db"

try:
    conn = sqlite3.connect(file)
    print("Database db\database.db formed.")
except:
    print("Database db\database.db not formed.")
