import sqlite3

try:
    conn = sqlite3.connect("register.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    myuser=cur.fetchall()
    print(myuser)
except sqlite3.Error as e:
            print(f"sqlite3 error:\n{e}")