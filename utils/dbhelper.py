import sqlite3

def getCursorFromFile(f):
    global conn
    global cur
    conn = sqlite3.connect(f, check_same_thread=False)
    cur = conn.cursor()

def execQuery(q, params):
    cur.execute(q, params)
    conn.commit()

def viewAccounts():
    cur.execute("SELECT * FROM ACCOUNTS")
    return cur.fetchall()

def getNewId(table):
    cur.execute("SELECT * FROM " + table)
    all_entries = cur.fetchall()
    ids = [entry[0] for entry in all_entries]
    if len(ids) > 0:
        return max(ids) + 1
    else:
        return 0

def nameAvailable(uname):
    cur.execute('SELECT USRNAME FROM ACCOUNTS WHERE USRNAME == "?"', (uname,))
    return cur.fetchone() == None

def checkLogin(uname, hashpw):
    cur.execute('SELECT * FROM ACCOUNTS WHERE USRNAME == "?" AND HASHPASS == "?"', (uname,hashpw))
    result = cur.fetchone()
    return result

