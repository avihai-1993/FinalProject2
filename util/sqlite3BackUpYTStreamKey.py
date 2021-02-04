import sqlite3

class SqlLiteKeyBackUp:

    def __init__(self):
        self.conn = sqlite3.connect('KEYBACKUP.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('''CREATE TABLE keysbackup (key text ,typeofvid text)''')

        except Exception as e:
            print("table exists")

    def addKey(self,key,typeofvid):
        self.conn = sqlite3.connect('KEYBACKUP.db')
        if not self.isKey(key):
            self.cursor.execute("INSERT INTO keysbackup (key,typeofvid) VALUES (?,?)", (key,typeofvid,))
            self.conn.commit()
            self.conn.close()

    def isKey(self,key):
        for row in self.cursor.execute('SELECT key FROM keysbackup where key = (?)', (key,)):
           if row[0] == key:
               return True

        return False


    def getAllkeys(self):
        keys = []
        for row in self.cursor.execute('SELECT * FROM keysbackup'):
            keys.append({"key" : row[0] , "type" : row[1]})
        return keys

    def delete(self,key):
        self.conn = sqlite3.connect('KEYBACKUP.db')
        self.cursor.execute("DELETE FROM keysbackup WHERE key = (?)", (key,))
        self.conn.commit()
        self.conn.close()

    def deleteKeys(self,keys):
        for k in keys:
            self.delete(k)



