import MySQLdb
import datetime
import math
from collections import deque
from prettytable import from_db_cursor

#run SQL SERVER FIRST AND RUN project.sql THEN RUN THIS
db = MySQLdb.connect(host="localhost",
           user="root",         # your username
           passwd="password",  # your password
           db="project")        # name of the data base
cur = db.cursor()
cur.autocommit = True
# you must create a Cursor object. It will let
#  you execute all the queries you need
def mysqlquery(query):
  cur.execute(query)

def printmysqlquery(query):
  cur.execute(query)
  table = from_db_cursor(cur)
  print(table)

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
    printmysqlquery("Select ID, Name From Product")
    id = input('Select Product via ID Number : ')
    mysqlquery  ("""
          Select Base_Cost, Name, ID From Product
          WHERE ID = '%s'
          """ %id)
    
    data = cur.fetchall()
    price = data[0][0]
    size = raw_input("""
                    Small   $'%s' (s)
                    Medium  $'%s' (m)
                    Large   $'%s' (l)
                    """%(price, round(price * 1.25, 2),
                         round(price * 1.75, 2)))
    if size == 'm':
      price = round(price * 1.25,2)

    if size == 'l':
      price = round(price * 1.75,2)
      
    name = data[0][1]
    prod_id = data[0][2]
    print(name,"$", price)
    total = price + total
    pretotal = total
    total = total + total * .26
    print "Total", total
    addmore = raw_input('Add more? (y,n,(r)emove an item')      
    receipt.append([])
    receipt[items].append(name)
    receipt[items].append(float(price))
    receipt[items].append(int(prod_id))
    items = items + 1
    if addmore == 'r':
        print("Item ID to Remove")
        i = 0
        for info in receipt:
          print(i, info)
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
  # mysqlquery("""
  #           Select MAX(Order_Num)
  #           """)
  db.commit()
  '''Payment Info'''
  pay = 0
  while pay != 1 and pay != 2:
    pay = input("""
              1. Cash
              2. Card
              """)
  maxordernum  = 1

  printmysqlquery("select * from Payment")
  mysqlquery("select Max(Order_Num) from Payment")
  maxordernum = cur.fetchall()[0][0]
  if not maxordernum:
    maxordernum = 1
  else :
    maxordernum = maxordernum + 1 
  print(maxordernum)
  ordernum = maxordernum
  print(ordernum)



  if pay == 1:
    cash = 0
    while cash < total:
      cash = input("""
                  Paid $
                  """)
    
    print("Change Owed $",(cash - total))
    
    mysqlquery("""
          Update CashInDrawer
          set Cash = '%s'
          """%(cash - total))
    printmysqlquery("select * from Payment") 

    mysqlquery("""
              Insert into Payment
              (Phone_Num, Order_Num, Type)
              Values('%s','%s','Cash')
              """%(custnum, ordernum))
    printmysqlquery("select * from Payment") 

  if pay == 2:
    printmysqlquery("select * from Payment") 
    print("Pay with Card")
    card_num = '0'
    while len(card_num) != 16:
      card_num = raw_input("Card Number")
      mysqlquery("""
                Insert into Payment
                (Phone_Num, Order_Num, Type, Card_Num)
                Values('%s','%s','Card', '%s')
                """%(custnum, ordernum, card_num))
    printmysqlquery("select * from Payment") 

  db.commit()
  print("Payment")

  mysqlquery("""    
            Insert into CustOrder(
            ID, Order_Num, Total, Tax, 
            Order_Cost
            )
            Values('%s','%s','%s','%s','%s')
            """
            %(custnum, ordernum, total, (total - pretotal),
            pretotal))
  print("Payment")
  print(receipt)
  printmysqlquery("select * from Order_Products")
  print(ordernum)
  for i in range(0, items):
      mysqlquery("""
                Insert into Order_Products(
                Cust_Num, Order_Num, Prod_id, Prod_cost)
                Values('%s', '%s', '%s' ,'%s')
                """
                %(custnum, ordernum, receipt[i][2], receipt[i][1]))
  printmysqlquery("select * from Order_Products")

  db.commit()
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
  
  db.commit()
    
def addprod():
  repeat = 'y'
  while repeat == 'y':
    new_prod = raw_input("Name of New Product ")
    prod_type = raw_input("Type of Product ")
    prod_cost = input("Base Cost of New Product ")
    prod_usage = input("Base Usage of Stock Unit ")

    printmysqlquery("""
              Select Max(ID) from Product 
              """)
    mysqlquery("""
              Select Max(ID) from Product 
              """)
    data = cur.fetchone()
    prod_id = data[0] + 1
    print(prod_id)
    mysqlquery("""
              Insert into Product(ID, Name, Type, Base_Cost, Base_Usage)
              Values('%s','%s','%s','%s','%s')
              """%(prod_id, new_prod, prod_type, prod_cost, prod_usage))
    printmysqlquery("select * from Product")
    db.commit()
    inglist = []
    printmysqlquery("Select * from Stock")
    mysqlquery("Select * from Stock")
    ing = 1
    while ing != 0:
      ing = input("Select ingredients to use 0 for done")
      inglist.append(ing)
    print(inglist)
    print(prod_id)
    for i in range(0, len(inglist)-1):
      mysqlquery("""
              Insert into StockInfo(Prod_id, Stock_id)
              Values('%s', '%s')
              """%(prod_id,inglist[i]))
    repeat = raw_input("Enter Another Product? (y/n)")


def stockedit(choice = -1):
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
print("""
-----Phill and Devinda's-----
---Pizza Management System---
------------v1.0-------------
""")
while choice != 0:
  print("""
    1. Order
    2. Edit Stock
    3. Add Product
    4. MySQL Query
    5. Commit
    0. Exit
    """)
  choice = input()
  #Switch Case
  if choice == 1: #ADD TO ORDER
    order()
  if choice == 2:
    stockedit()
  if choice == 3:
    addprod()
  if choice == 4:
    query = raw_input("mysql>")
    printmysqlquery(query)
  if choice == 5:
    db.commit()
  if choice == 6:
    addingredients()
  if choice == 0:
    break



# print all the first cell of all the rows
#for row in cur.fetchall():
 #   print (row[2])
if raw_input('Commit?') == 'y':
  db.commit()
db.close()