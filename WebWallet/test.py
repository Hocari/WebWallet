import sqlite3


# Connect to the database (creates the database file if it doesn't exist)
conn = sqlite3.connect("user_data.db")
while True:
    username = input("Username?: ")

    # Create a cursor to execute SQL commands
    c = conn.cursor()

    # Create a new table for the user's data
    c.execute("CREATE TABLE IF NOT EXISTS {} (username TEXT, subject TEXT, body TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)".format(username))

    # Commit the changes to the database and close the connection
    conn.commit()


