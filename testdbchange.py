import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

params = ("Trevor", "22.22", "22.22")
# statement = f"SELECT 'True' FROM NMPOOL2485Location WHERE UName = {uname}"

c.execute("INSERT or ignore into NMPOOL2485Location(UName, Latitude, Longitude) VALUES(?,?,?)", params)
c.execute("update NMPOOL2485Location set Latitude = ?, Longitude = ? where Uname = ?", params)


conn.commit()