import MySQLdb

db = MySQLdb.connect(host="localhost",
           user="root",         # your username
           passwd="password",  # your password
           db="project")        # name of the data base
cur = db.cursor()

# you must create a Cursor object. It will let
#  you execute all the queries you need
def mysqlquery(query):
  cur.execute(query)

def printmysqlquery(query):
  cur.execute(query)
  for info in cur:
    print info

def newcust():
  custname = raw_input('Cust Name:')
  cust_num = input('Cust Num:')
  cur.execute(
        """Insert into Customer
        (Phone_num, Name)
        Values(%s,%s)""",
        [cust_num, custname])

def order():
  total = 0
  addmore = 'y'
  items = 0
  receipt = []
  while addmore == 'y':
    printmysqlquery("Select ID, Name, Base_Cost From Product")
    id = input('Select Product via ID Number : ')
    mysqlquery  ("""
          Select Base_Cost, Name, ID From Product
          WHERE ID = '%s'
          """ %id)
    data = cur.fetchall()
    price = data[0][0]
    name = data[0][1]
    prod_id = data[0][2]
    print(name, price)
    total = price + total
    print "Total", total
    addmore = raw_input('Add more? (y,n)')
    receipt.append([])
    receipt[items].append(name)
    receipt[items].append(float(price))
    receipt[items].append(int(prod_id))
    items = items + 1
  receipt.append("Total : " + str(total))
  print(receipt)
  custnum = input("Enter Customer Number : ")
  mysqlquery  ("""
        Select Name From Customer
        Where Phone_Num = '%s'
        """ %custnum)
  if cur.rowcount == 0 :
    print("User Not Found")
    print("New Customer Info")
    newcust()
  else:
    cust_name = cur.fetchall()[0]
    print(cust_name)
    
  ''' Updates Stock '''
  for i in range(0,items):
    mysqlquery("""
              Select d.ID, d.Av_Quan - e.Base_Usage 
            	From (Select a.Base_Usage, b.Prod_id, b.Stock_id 
				      From StockInfo as b, Product as a 
				      Where a.ID = '%s' and a.ID = b.Prod_id) 
	            e, Stock d
	            Where d.ID = e.Stock_id
              """%int(receipt[i][2]))
    stock = cur.fetchall()
    for j in range(0, len(stock)):
      mysqlquery("""
                Update Stock
                set Av_Quan = '%s'
                Where Stock.ID = '%s'
                """%(stock[j][1], stock[j][0]))
    
    
def stockedit():
  choice = -1
  while choice != 0:
    print   ("""
    1. View Stock
    2. Edit Existing
    3. Add New Stock
    0. Exit
        """)
    choice = input()
    if choice == 1:
      printmysqlquery("""
              SELECT * From Stock
              """)
    if choice == 2:
      printmysqlquery ("""
              SELECT *
              From Stock
              """)
      data = list(cur.fetchall())
      id = input("Enter ID of Stock to be Edited")
      printmysqlquery("""
              Select Item, Av_Quan
              From Stock
              Where ID = '%s'
              """ %id)
      mod = input("""Number to be added to
            available quantity
            Negative or positive""")
      mysqlquery  ("""
            Update Stock Set Av_Quan = Av_Quan +'%s'
            Where ID = '%s'
            """%(mod,id))
    if choice == 3:
      printmysqlquery ("""
              SELECT *
              From Stock
              """)
      id = input("Id number of new stock number")
      item = raw_input("Name of Product")
      type = raw_input("Type of Stock Item")
      quan = input("Available Quantity")
      mysqlquery  ("""
            Insert into Stock(ID, Item, Type, Av_Quan)
            Values('%s', '%s', '%s', '%s')
            """%(id, item, type, quan))
  
#END FUNCTION DEFINITIONS 
choice = -1
while choice != 0:
  print("""
    1. Order
    2. Edit Stock
    3. MySQL Query
    4. Commit
    0. Exit
    """)
  choice = input()
  #Switch Case
  if choice == 1: #ADD TO ORDER
    order()
  if choice == 2:
    stockedit()
  if choice == 3:
    query = input("mysql>")
    mysqlquery(query)
  if choice == 4:
    db.commit()
  if choice == 0:
    break



# print all the first cell of all the rows
#for row in cur.fetchall():
 #   print (row[2])
if raw_input('Commit?') == 'y':
  db.commit()
db.close()