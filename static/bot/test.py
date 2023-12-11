import sqlite3

database = "workerbase.db"

idlist = []
id = 1140715870
idlist.append((id,))
idlist.append((5019442968,))
#text = tuple(idlist)
#idlist = [(1140715870,), (5019442968,)]
print(idlist)

con = sqlite3.connect(database)
cur = con.cursor()
cur.executemany("DELETE FROM workers WHERE id = ?",(idlist))
con.commit()

