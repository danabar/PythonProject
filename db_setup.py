from flask import Flask 
from flask_mysqldb import MySQL
from datetime import datetime
import uuid
app = Flask(__name__)
mysql = MySQL(app)
def db_init(app):
 app.config['MYSQL_HOST'] = 'localhost'
 app.config['MYSQL_USER'] = 'root'
 app.config['MYSQL_PASSWORD'] = 'root'
 app.config['MYSQL_DB'] = 'shop'
 mysql = MySQL(app)
 
def insert_product(product_name , product_expire_date , product_size): 
 product_id = uuid.uuid1()
 cur = mysql.connection.cursor()
 cur.execute("INSERT INTO product(product_id, product_name , product_expire_date , product_size) VALUES (%s, %s , %s, %s)", (product_id.hex, product_name , product_expire_date , product_size))
 mysql.connection.commit()
 cur.close()
 
def insert_location(city , street , building_number): 
 location_id = uuid.uuid1()
 cur = mysql.connection.cursor()
 cur.execute("INSERT INTO location(location_id, city , street , building_number) VALUES (%s, %s ,%s, %s)", (location_id.hex,city , street , building_number))
 mysql.connection.commit()
 cur.close()
 
def insert_product_movment(product_id , from_location , to_location): 
 movement_id = uuid.uuid1()
 cur = mysql.connection.cursor()

 if  not from_location and  to_location :
    cur.execute("INSERT INTO productmovement (movement_id, product_id , to_location) VALUES (%s, %s , %s)", (movement_id.hex , product_id , to_location))
 elif   from_location and not to_location :
     cur.execute("INSERT INTO productmovement (movement_id, product_id , from_location) VALUES (%s, %s , %s)", (movement_id.hex , product_id , from_location ))
 elif  not from_location and not to_location :
     cur.execute("INSERT INTO productmovement (movement_id, product_id ) VALUES (%s, %s )", (movement_id.hex , product_id))
 else:
     cur.execute("INSERT INTO productmovement (movement_id, product_id , from_location ,to_location) VALUES (%s, %s , %s , %s)", (movement_id.hex , product_id , from_location , to_location))
	 
 mysql.connection.commit()
 cur.close()
 
def select_product(product_id): 
 cur = mysql.connection.cursor()
 result = cur.execute("Select * from product where product_id = %s)", (product_id))
 mysql.connection.commit()
 cur.close()
 return result
 
def select_all_product(): 
 cur = mysql.connection.cursor()
 result = cur.execute("Select * from product")
 result = cur.fetchall()
 mysql.connection.commit()
 cur.close()
 return result
 
def select_all_location(): 
 cur = mysql.connection.cursor()
 result = cur.execute("Select * from location")
 result = cur.fetchall()
 mysql.connection.commit()
 cur.close()
 return result
 
def select_all_movement(): 
 cur = mysql.connection.cursor()
 result = cur.execute("SELECT m.movement_id, m.product_id , p.product_name ,(select concat(tl.city , ' - ', tl.street , ' - ', tl.building_number) from location tl where tl.location_id= m.to_location) as to_location ,(select concat(fl.city , ' - ', fl.street , ' - ', fl.building_number) from location fl  where fl.location_id= m.from_location) as from_location  FROM shop.location l  join shop.productmovement m on l.location_id = m.from_location or l.location_id = m.to_location  join shop.product p on m.product_id = p.product_id")
 result = cur.fetchall()
 mysql.connection.commit()
 cur.close()
 return result
 
def select_location(location_id): 
 cur = mysql.connection.cursor()
 result = cur.execute("select * from location where location_id = %s ", (location_id))
 mysql.connection.commit()
 cur.close()
 return result
 
def select_product_movment(product_name): 
 sid = uuid.uuid1()
 cur = mysql.connection.cursor()
 result = cur.execute("INSERT INTO product(product_id, product_name) VALUES (%s, %s)", (sid.hex, product_name))
 mysql.connection.commit()
 cur.close()
 return result
 
def update_product(product_id , product_name , product_expire_date , product_size): 
 uid = uuid.uuid1()
 cur = mysql.connection.cursor()
 cur.execute("update product set product_name = %s , product_expire_date = %s , product_size = %s Where product_id = %s ", (product_name , product_expire_date , product_size , product_id))
 mysql.connection.commit()
 cur.close()
 
 
def update_location(location_id , city , street , building_number ): 
 cur = mysql.connection.cursor()
 result = cur.execute("Update location set city = %s , street = %s , building_number = %s Where location_id = %s ", (city , street , building_number , location_id))
 mysql.connection.commit()
 cur.close()
 return result

 
def update_product_movement(movement_id , product_id , from_location , to_location): 
 id = uuid.uuid1()
 cur = mysql.connection.cursor()
 print("  " + product_id +"  " + from_location +"  " + to_location)
 if not from_location and  to_location :
    cur.execute("update productmovement set product_id = %s , from_location = null , to_location = %s where movement_id = %s", (product_id , to_location , movement_id))
 elif  from_location  and not to_location :
    cur.execute("update productmovement set product_id = %s , from_location = %s , to_location = null where movement_id = %s", (product_id , from_location , movement_id))
 elif  not from_location  and  not to_location :
    cur.execute("update productmovement set product_id = %s , from_location = null , to_location = null where movement_id = %s", (product_id , movement_id))
 else:
    cur.execute("update productmovement set product_id = %s , from_location = %s , to_location = %s where movement_id = %s", (product_id , from_location , to_location , movement_id))

 mysql.connection.commit()
 cur.close()
 
def select_all_product_movement_count():
 cur = mysql.connection.cursor()
 cur.execute("SELECT  p.product_name ,(select concat(fl.city , ' - ', fl.street , ' - ', fl.building_number) from location fl  where fl.location_id= m.from_location) as from_location   ,count(m.product_id) as Qty FROM shop.location l   join shop.productmovement m on l.location_id = m.from_location  join shop.product p on m.product_id = p.product_id group by m.from_location ")
 result = cur.fetchall()
 mysql.connection.commit()
 cur.close()
 return result
