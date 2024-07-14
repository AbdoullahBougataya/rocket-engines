# Importing Sqlite3 Module
import sqlite3

try:
	# Making a connection between sqlite3 database and Python Program
	con = sqlite3.connect('db\database.db')
	# If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
	# Otherwise it will show errors
	print("Connected to SQLite")
except sqlite3.Error as error:
	print("Failed to connect with the sqlite3 database", error)
finally:
	# Inside Finally Block, If connection is open
	if con:
		cur = con.cursor()
		# using close() method, we will close the connection
		con.close()
		# After closing connection object, we will print "the sqlite connection is closed"
		print("the sqlite connection is closed")
