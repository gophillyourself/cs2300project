#mysql

drop database project;

CREATE DATABASE project;

use project;

CREATE TABLE CustOrder(
	ID 			int(10) 	primary key,
	Total 		double 		NOT NULL,
	Tax			double 		NOT NULL,
	Order_Cost 	double 		NOT NULL,
	Order_time	time 		NOT NULL,
	Owed		double 		NOT NULL
);

CREATE TABLE Customer(
	Phone_Num 	decimal(10)		primary key,
	Name 		varchar(80)		NOT NULL,
	Amount_Paid	double			NOT NULL
);

CREATE TABLE Payment(
	Phone_Num 	decimal(10) 	NOT NULL,
	Order_Num	int				NOT NULL,
	Type 		varchar(4) 		NOT NULL,
		CHECK(	Type = 'Card' OR
				Type = 'Cash'),
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
	Base_Usage	double		NOT NULL,
	Total		double		NOT NULL
);
INSERT into Product
	Values(	1, 		'Peperoni Pizza', 'Pizza',
			7.50, 	2,	)

CREATE TABLE Stock(
	ID			int			primary key,
	Item		varchar(20)	NOT NULL,
	Type		varchar(20)	NOT NULL,
	Av_Quan		int			NOT NULL
);

#initializer
INSERT INTO Stock	(ID, Item, Type, Av_Quan)
	VALUES			(4, 'Peperoni', 'Topping', 4),
					(5, 'Coke',		'SodaBIB', 2);

CREATE TABLE Order_Products(
	Phone_Num 	decimal(10) 	NOT NULL,
	Order_Num	int				NOT NULL,
	Prod_id		int				NOT NULL,
	Size		varchar(1)		NOT NULL,
		CHECK(	SIZE = 'S' OR
				SIZE = 'M' OR
				SIZE = 'L'),
	Additions	varchar(20),
	Add_cost	decimal,
	PRIMARY KEY(Phone_Num, Order_Num),
	FOREIGN KEY(Order_Num) references 	CustOrder(ID),
	FOREIGN KEY(Phone_Num) references 	Customer(Phone_Num),
	FOREIGN KEY(Prod_id) 	references	Product(ID)
);

CREATE TABLE StockInfo(
	Prod_id		int 		NOT NULL,
	Stock_id	int			NOT NULL,
	Base_Usage	decimal		NOT NULL,
	FOREIGN KEY(Prod_id)	references Product(ID),
	FOREIGN KEY(Stock_id) 	references Stock(ID)
	);

