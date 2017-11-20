import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="password",  # your password
                     db="project")        # name of the data base
cur = db.cursor()

# you must create a Cursor object. It will let
#  you execute all the queries you need
def mysqlquery(query):
    cur.execute(query)
    for info in cur:
        print info

def newcust():
    custname = raw_input('Cust Name:')
    cust_num = input('Cust Num:')
    cust_paid = input('Paid $:')
    cur.execute(
                """Insert into Customer
                (Phone_num, Name, Amount_Paid) 
                Values(%s,%s,%s)""",
                [cust_num, custname, cust_paid])

def addtoorder():
    mysqlquery("Select ID, Name, Base_Cost From Product")
    id = input('Select Product via ID Number')
    mysqlquery  ("""
                Select Base_Cost From Product
                WHERE ID = '%s'
                """ %id)
    data = cur.fetchone()[0]
    print(data)

choice = -1
while choice != 0:
    print("""
        1. New Customer 
        2. Add to Order
        3. Edit Stock
        4. MySQL Query
        5. Commit
        0. Exit
        """)
    choice = input()
    #Switch Case
    if choice == 1: #NEW CUSTOMER
        newcust()
    if choice == 2: #ADD TO ORDER
        addtoorder()
    if choice == 3: 
        print "Coming Soon"
    if choice == 4: 
        query = input("mysql>")
        mysqlquery(query)
    if choice == 5:
        db.commit()
    if choice == 0:
        break
    
    

# print all the first cell of all the rows
#for row in cur.fetchall():
 #   print (row[2])
if input('Commit?') == 'y':
    db.commit()
db.close()