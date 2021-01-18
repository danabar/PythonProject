from flask import Flask , render_template , request
from db_setup import db_init , select_all_product , select_all_location , select_all_movement , insert_product , update_product , insert_location, select_all_product_movement_count , update_location , insert_product_movment , update_product_movement
app = Flask(__name__)
db_init(app)
@app.route("/")
def home():
    return render_template("mainPage.html")


@app.route("/product/")
def product():
    headings = ("Product_id","Product_Name","Product_Expir_Date", "Product_size")
    data = select_all_product()
    return render_template("products.html" , headings=headings , data=data)

@app.route("/location/")
def location():
    headings = ("Location_id","City","Street", "Building_Number")
    data = select_all_location()
    return render_template("locations.html" , headings=headings , data=data)
	
@app.route("/movement/")
def movement():
    headings = ("Movement_id","Product_id","Product_Name","From_Location", "To_Location")
    data = select_all_movement()
    products_options = select_all_product()
    locations_options = select_all_location()
    return render_template("movements.html" , headings=headings , data=data , products_options=products_options , locations_options=locations_options )

@app.route("/report/")
def report():
    headings = ("Product_Name","Warehouse" , "Qty")
    data = select_all_product_movement_count()
    return render_template("report.html" , headings=headings , data=data)
	
@app.route("/add_edit_product/",methods = ['POST', 'GET'])	
def add_edit_product():
   if(request.form.get("product-id") == ""):
     insert_product(request.form.get("product-name") , request.form.get("product-expire-date"), request.form.get("product-size"))
   else:
     update_product(request.form.get("product-id").strip() , request.form.get("product-name") , request.form.get("product-expire-date"), request.form.get("product-size"))
	 
   return product()

	
@app.route("/add_edit_location/",methods = ['POST', 'GET'])	
def add_edit_location():
   if(request.form.get("location-id") == ""):
     insert_location(request.form.get("city") , request.form.get("street"), request.form.get("building-number"))
   else:
     update_location(request.form.get("location-id").strip() , request.form.get("city") , request.form.get("street"), request.form.get("building-number"))
	 
   return location()
   	
@app.route("/add_edit_movement/",methods = ['POST', 'GET'])	
def add_edit_movement():
   if(request.form.get("movement-id") == ""):
     insert_product_movment(request.form.get("select-product") , request.form.get("select-from-location"), request.form.get("select-to-location"))
   else:
     update_product_movement(request.form.get("movement-id").strip() , request.form.get("select-product") , request.form.get("select-from-location"), request.form.get("select-to-location"))
	 
   return movement()

    
	
if __name__ == '__main__':
    app.run()