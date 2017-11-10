require 'mysql2'

#my = Mysql.new(hostname, username, password, databasename)  
con = Mysql2::Client.new(:host => "localhost",
						 :username => "root",
						 :password => "password",
						 :database => "project")

con.query("select * from StockInfo;").each do |row|
end 
#rs.each_cons{ |h| puts h['Prod_id']}  


con.close  
