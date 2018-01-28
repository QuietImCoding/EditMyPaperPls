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
    cur.execute("SELECT * FROM ACCOUNTS WHERE USRNAME = ?", (uname,))
    result = cur.fetchone()
    return result is None


def getPWHash(uname):
    cur.execute("SELECT HASHPASS FROM ACCOUNTS WHERE USRNAME = ?", (uname,))
    result = cur.fetchone()
    print("PASSHASH :", result)
    if result is not None:
        return result[0]
    else:
        return result

def getAuthorName(author_id):
    cur.execute("SELECT USRNAME FROM ACCOUNTS WHERE ID = ?", (author_id,))
    result = cur.fetchone()
    return result[0]


def getUserID(username):
    cur.execute("SELECT ID FROM ACCOUNTS WHERE USRNAME = ?", (username,))
    result = cur.fetchone()
    print("FOUND USER WITH ID", str(result))
    return result[0]

def getEssay(paper_id):
    cur.execute("SELECT * FROM PAPERS WHERE PAPER_ID = ?", (paper_id,))
    result = cur.fetchone()
    essay = {}
    essay["title"] = result[2]
    essay["content"] = result[3]
    essay["author"] = getAuthorName(result[1])
    print(result)
    return essay
