#mysql

drop database project;

CREATE DATABASE project;

use project;
#TODO Relate CustOrder to Order_products

CREATE TABLE CustOrder(
	ID 					int(10) 							primary key,
	Order_Num		int Default 1 				primary key,
	Total 			double 								NOT NULL,
	Tax					double 								NOT NULL,
	Order_Cost 	double 								NOT NULL,
	Order_time	time 									NOT NULL,
	Order_date	date 									NOT NULL
);

CREATE TABLE Customer(
	Phone_Num 	decimal(10)		primary key,
	Name 		varchar(80)		NOT NULL,
	Amount_Paid	double			
);

CREATE TABLE Payment(
	Phone_Num 	decimal(10) 	NOT NULL,
	Order_Num	int				NOT NULL,
	Type 		enum('Card', 'Cash'),
	Amount 		double,
	Card_Num	int(16), #TODO add condition for int 
						 #being not allowed null if Type = Cast
	PRIMARY KEY(Phone_Num, Order_Num),
	FOREIGN KEY(Order_Num) references CustOrder(ID),
	FOREIGN KEY(Phone_Num) references Customer(Phone_Num)
);

CREATE TABLE Product(
	ID 			int			primary key,
	Name		varchar(20)	NOT NULL,
	Type 		varchar(20)	NOT NULL,
	Base_Cost	double		NOT NULL,
	Base_Usage	double		NOT NULL
);

INSERT into Product	(ID, Name, Type, Base_Cost, Base_Usage)
	Values	(1, 'Cheese Pizza', 'Pizza', 7.50, 1),
					(2,	'Pepperoni Pizza', 'Pizza', 8.50, 1),
					(3,	'Sausage Pizza',	'Pizza',	8.50,	1)
					(4, 'Soda',	'Soda',	1.10, .25);

CREATE TABLE Stock(
	ID			int			primary key,
	Item		varchar(20)	NOT NULL,
	Type		varchar(20)	NOT NULL,
	Av_Quan		double			NOT NULL
);

#initializer
INSERT INTO Stock	(ID, Item, Type, Av_Quan)
	VALUES	(1,	'Dough',	'Base',				5),
					(2,	'Cheese',	'Topping',		6),
					(3,	'Red',		'Sauce',			7),
					(4, 'Peperoni', 'Topping',	4),
					(5, 'Coke',		'SodaBIB', 		2),
					(6, 'Pepsi',	'SodaBIB',		9),
					(7, 'Sausage','Topping',		10);

CREATE TABLE Order_Products(
	Phone_Num 	decimal(10) 	NOT NULL,
	Order_Num	int				NOT NULL,
	Prod_id		int				NOT NULL,
	Size			enum('S', 'M', 'L'),
	Prod_cost double		NOT NULL,
	PRIMARY KEY(Phone_Num,	Order_Num),
	FOREIGN KEY(Order_Num)	references 	CustOrder(ID),
	FOREIGN KEY(Phone_Num) 	references 	Customer(Phone_Num),
	FOREIGN KEY(Prod_id)		references	Product(ID),
	FOREIGN KEY(Order_Num)	references	CustOrder(Order_Num)
);

CREATE TABLE StockInfo(
	Prod_id		int 		NOT NULL,
	Stock_id	int			NOT NULL,
	#Base_Usage	decimal		,
	FOREIGN KEY(Prod_id)	references Product(ID),
	FOREIGN KEY(Stock_id) 	references Stock(ID)
	);

INSERT INTO StockInfo
					(Prod_id, Stock_id)
	VALUES	(1, 1), #1 is cheese pizza
					(1, 2),
					(1, 3),
					(2, 1), #2 is pepperoni
					(2, 2),
					(2, 3),
					(2, 4),
					(3, 1), #3 Sausage pizza
					(3, 2),
					(3, 3),
					(3, 7),
					(4, 5);
/*CREATE TABLE Ingredients(
	Prod_ID	int NOT NULL,
	Seq_Num int NOT NULL,
	Ingr_ID	int	NOT NULL,
	Name 		varchar(20) NOT NULL
	FOREIGN KEY(Prod
); 
