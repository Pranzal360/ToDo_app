import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        #Create a cursor 
        self.c = self.conn.cursor()
        #calling Table
        self.create_table1
        self.create_table1
        self.create_table3
    #list to add

    # create a table for page 1
    def create_table1(self):
        self.c.execute("""CREATE TABlE IF NOT EXISTS tab1(
            ItemName text,
            Cost text,
            date text
        )
        """)
        self.conn.commit()
        return "Created"


    # inserting into database for page 1
    def addIntoDB1(self,value):
        self.c.executemany("INSERT INTO tab1 VALUES(?,?,?)",value,)
        self.conn.commit()

    #  Getting the values for table1 
    def fetchData1(self):
        outs = self.c.execute("SELECT rowid,* FROM tab1").fetchall()
        return outs

    def deleteData1(self,taskid):
        self.c.execute("DELETE FROM tab1 where rowid = ?",(taskid,) )
        self.conn.commit() 
        
