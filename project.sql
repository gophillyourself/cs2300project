#mysql

drop database project;

CREATE DATABASE project;

use project;

CREATE TABLE CustOrder(
	ID 			int(10) 	primary key,
	Total 		decimal 	NOT NULL,
	Tax			decimal 	NOT NULL,
	Order_Cost 	decimal 	NOT NULL,
	Order_time	time 		NOT NULL,
	Owed		decimal 	NOT NULL
);

CREATE TABLE Customer(
	Phone_Num 	int(10)		primary key,
	Name 		varchar(80)	NOT NULL,
	Amount_Paid	decimal		NOT NULL
);

CREATE TABLE Payment(
	Phone_Num 	int(10) 	NOT NULL,
	Order_Num	int			NOT NULL,
	Type 		varchar(4) 	NOT NULL,
		CHECK(	Type = 'Card' OR
				Type = 'Cash'),
	Amount 		decimal,
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
	Base_Cost	decimal		NOT NULL,
	Base_Usage	decimal		NOT NULL,
	Multiplier	decimal		NOT NULL,
	Total		decimal		NOT NULL
);

CREATE TABLE Stock(
	ID			int			primary key,
	Item		varchar(20)	NOT NULL,
	Type		varchar(20)	NOT NULL,
	Av_Quan		int			NOT NULL
);

#inintializer
INSERT INTO Stock	(ID, Item, Type, Av_Quan)
	VALUES			(4, 'Peperoni', 'Topping', 4),
					(5, 'Coke',		'SodaBIB', 2);

CREATE TABLE Order_Products(
	Phone_Num 	int(10) 	NOT NULL,
	Order_Num	int			NOT NULL,

	Prod_id		int			NOT NULL,
	Size		varchar(1)	NOT NULL,
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

