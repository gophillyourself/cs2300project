import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="password",  # your password
                     db="project")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
repeat = 'y'

while repeat == 'y':
    #Customer table
    custname = raw_input('Cust Name:')
    cust_num = raw_input('Cust Num:')
    cust_paid = raw_input('Paid $:')

    cur.execute("""
                Insert into Customer
                (Phone_num, Name, Amount_Paid) 
                Values"""(cust_num ","
                custname ","
                cust_paid")")

# print all the first cell of all the rows
for row in cur.fetchall():
    print (row[2])

db.close()