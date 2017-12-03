#Form to insert a post order record 

Insert into CustOrder
		(ID, Order_Num, Total, 
		Tax, Order_Cost, Order_time, Order_date)
Values(/*Customer ID*/, MAX(Order_Num)+1, 
			/*Calculated Total*/, /*Tax*/, 
			select ,
			TIME, date);

#new Customer
Insert into Customer
  (Phone_num, Name)
  Values(%s,%s)

#list products for selection
Select Base_Cost, Name, ID From Product
  WHERE ID = '%s'

#checking for existing customer by number
Select Name From Customer
  Where Phone_Num = '%s'

#updating stock

Select d.ID, d.Av_Quan - e.Base_Usage 
  From (Select a.Base_Usage, b.Prod_id, b.Stock_id 
  From StockInfo as b, Product as a 
  Where a.ID = '%s' and a.ID = b.Prod_id) 
  e, Stock d
  Where d.ID = e.Stock_id

Update Stock
  set Av_Quan = '%s'
  Where Stock.ID = '%s'

#lists stock
Select a.ID, a.Name, b.ID, b.Item, b.Av_Quan,  
  From Product a, Stock b, StockInfo c  
  Where a.ID = c.Prod_id AND c.Stock_id = b.ID;