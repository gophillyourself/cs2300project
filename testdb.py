import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="password",  # your password
                     db="project")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
repeat = 'y'

cur.execute("SHOW TABLES")


tables = cur.fetchall()
while repeat == 'y':
    #Customer table
    custname = raw_input('Cust Name:')
    cust_num = input('Cust Num:')
    cust_paid = input('Paid $:')

    cur.execute(
                """Insert into Customer
                (Phone_num, Name, Amount_Paid) 
                Values(%s,%s,%s)""",
                [cust_num, custname, cust_paid])
                
    cur.execute("select * from Customer")
    for row in cur:
        print row
    repeat = raw_input('Anotha one?')
    

# print all the first cell of all the rows
#for row in cur.fetchall():
 #   print (row[2])

db.close()