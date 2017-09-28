import pymysql


class DatabaseConnector:

    def __init__(self, Host, Port, User, PassW, DatabaseName ):
        self.conn = pymysql.connect(host=Host, port=Port, user=User, passwd=PassW, db=DatabaseName)

    def select(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM actual_coindata")

        print(cur.description)
        print()

        for row in cur:
            print(row)

        cur.close()
        #self.conn.close()

    def insert(self):
         with self.conn.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `actual_coindata` (`long_name`) VALUES (%s)"
            cursor.execute(sql, ('test'))
            self.conn.commit()

    def closeConn(self):
        self.conn.close()

if __name__ == "__main__":
    con= DatabaseConnector('localhost',3306,'root','','coindata')

    con.insert()
    con.select()
    con.closeConn()
