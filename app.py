# READ ME:
#   All code is based on the CS 340 starter code, 
#   with the exception of the reference of Group 69's search feature in our own implementation of the search feature.
#
#   This project is a flask application with a frontend which is intended for internal use 
#   in order to manage the database for this fictional company. 

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)



app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_'
app.config['MYSQL_PASSWORD'] = '' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
# db_connection = db.connect_to_database()
mysql = MySQL(app)
# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            customer_name = request.form["customer_name"]
            date_created = request.form["date_created"]
            customer_email = request.form["customer_email"]
            customer_phone = request.form["customer_phone"]

            # account for null age
            if customer_phone == "":
                query = "INSERT INTO Customers (customer_name, date_created, customer_email) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_name, date_created, customer_email))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Customers (customer_name, date_created, customer_email, customer_phone) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_name, date_created, customer_email, customer_phone))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/customers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":

        browse_query = request.args
        # if search exists
        if browse_query:
            browse_query = browse_query['search']
            query = "SELECT * FROM Customers WHERE customer_name = '%s'" % (browse_query)
        # mySQL query to grab all the people in bsg_people
        else:
            query = "SELECT * FROM Customers"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("customers.j2", data=data)
    

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customer_id = '%s';" % (customer_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/customers")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_customer/<customer_id>", methods=["POST", "GET"])
def edit_customer(customer_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Customers WHERE customer_id = %s" % (customer_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_customers.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            customer_name = request.form["customer_name"]
            date_created = request.form["date_created"]
            customer_email = request.form["customer_email"]
            customer_phone = request.form["customer_phone"]

            # account for null homeworld
            if customer_phone == "":
                query = "UPDATE Customers SET Customers.customer_name = %s, Customers.date_created = %s, Customers.customer_email = %s, Customers.customer_phone = NULL WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_name, date_created, customer_email, customer_id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Customers SET Customers.customer_name = %s, Customers.date_created = %s, Customers.customer_email = %s, Customers.customer_phone = %s WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_name, date_created, customer_email, customer_phone, customer_id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/customers")
        
@app.route('/products', methods=["POST", "GET"])
def products():
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Product"):
            # grab user form inputs
            # query = "SELECT Manufacturers.manufacturer_id AS manufacturer_id FROM Manufacturers"
            # cur = mysql.connection.cursor()
            # cur.execute(query)
            # manufacturer_data = cur.fatchall()
            
            product_name = request.form["product_name"]
            product_price = request.form["product_price"]
            manufacturer_id = request.form["manufacturer_id"]

            query = "INSERT INTO Products (product_name, product_price, manufacturer_id) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_name, product_price, manufacturer_id))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/products")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Products.product_id, Products.product_name, Products.product_price, Manufacturers.manufacturer_name FROM Products LEFT JOIN Manufacturers ON Products.manufacturer_id = Manufacturers.manufacturer_id"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT manufacturer_id FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        manufacturer_data = cur.fetchall()

        return render_template("products.j2", data=data, manufacturer_data=manufacturer_data)
    


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Products WHERE product_id = %s" % (product_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/products")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
def edit_product(product_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Products WHERE product_id = %s" % (product_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT Manufacturers.manufacturer_name FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        manufacturer_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_products.j2", data=data, manufacturer_data=manufacturer_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Product"):
            # grab user form inputs
            product_name = request.form["product_name"]
            product_price = request.form["product_price"]
            manufacturer_name = request.form["manufacturer_name"]

            query = "UPDATE Products SET Products.product_name = %s, Products.product_price = %s, Products.manufacturer_id = (SELECT manufacturer_id FROM Manufacturers WHERE manufacturer_name = %s) WHERE Products.product_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_name, product_price, manufacturer_name, product_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/products")
        
@app.route('/invoices', methods=["POST", "GET"])
def invoices():
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Invoice"):
            # grab user form inputs
            # invoice_id = request.form["invoice_id"]
            customer_id = request.form["customer_id"]
            transaction_date = request.form["transaction_date"]
            total_price = request.form["total_price"]

            query = "INSERT INTO Invoices (customer_id, transaction_date, total_price) VALUES ( %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, ( customer_id, transaction_date, total_price))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/invoices")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * FROM Invoices"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        query2 = "SELECT customer_id FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customer_data = cur.fetchall()

        return render_template("invoices.j2", data=data, customer_data=customer_data)
    


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_invoice/<int:invoice_id>")
def delete_invoice(invoice_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Invoices WHERE invoice_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_id))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/invoices")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_invoice/<int:invoice_id>", methods=["POST", "GET"])
def edit_invoice(invoice_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Invoices WHERE invoice_id = %s" % (invoice_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT Customers.customer_id FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customer_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_invoices.j2", data=data, customer_data=customer_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Invoice"):
            # grab user form inputs
            # customer_id = request.form["customer_id"]
            transaction_date = request.form["transaction_date"]
            total_price = request.form["total_price"]

            query = "UPDATE Invoices SET transaction_date = %s, total_price = %s WHERE invoice_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (transaction_date, total_price, invoice_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/invoices")
        
@app.route('/manufacturers', methods=["POST", "GET"])
def manufacturers():
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Manufacturer"):
            # grab user form inputs
            manufacturer_name = request.form["manufacturer_name"]

            query = "INSERT INTO Manufacturers (manufacturer_name) VALUES ('%s')" % (manufacturer_name)
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            
            # redirect back to people page
            return redirect("/manufacturers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * FROM Manufacturers"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("manufacturers.j2", data=data)
    


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_manufacturer/<int:manufacturer_id>")
def delete_manufacturer(manufacturer_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Manufacturers WHERE manufacturer_id = %s" % (manufacturer_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/manufacturers")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_manufacturer/<int:manufacturer_id>", methods=["POST", "GET"])
def edit_manufacturer(manufacturer_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Manufacturers WHERE manufacturer_id = %s" % (manufacturer_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_manufacturers.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Manufacturer"):
            # grab user form inputs
            manufacturer_name = request.form["manufacturer_name"]

            query = "UPDATE Manufacturers SET Manufacturers.manufacturer_name = %s WHERE Manufacturers.manufacturer_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (manufacturer_name, manufacturer_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/manufacturers")
        
@app.route('/sales', methods=["POST", "GET"])
def sales():
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Sale"):
            # grab user form inputs
            invoice_id = request.form["invoice_id"]
            product_id = request.form["product_id"]
            quantity_sold = request.form["quantity_sold"]

            query = "INSERT INTO Sales (invoice_id, product_id, quantity_sold) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (invoice_id, product_id, quantity_sold))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/sales")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * FROM Sales"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        query2 = "SELECT invoice_id FROM Invoices"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        invoice_data = cur.fetchall()

        query3 = "SELECT product_id FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()
        
        return render_template("sales.j2", data=data, invoice_data=invoice_data, product_data=product_data)
    
# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_sale/<int:invoice_id>/<int:product_id>")
def delete_sale(invoice_id, product_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Sales WHERE invoice_id = '%s' AND product_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_id, product_id))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/sales")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_sale/<int:invoice_id>/<int:product_id>", methods=["POST", "GET"])
def edit_sale(invoice_id, product_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Sales WHERE invoice_id = %s AND product_id = %s" % (invoice_id, product_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_sales.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Sale"):
            # grab user form inputs
            product_id = request.form["product_id"]
            quantity_sold = request.form["quantity_sold"]

            query = "UPDATE Sales SET Sales.invoice_id = %s, Sales.product_id = %s, Sales.quantity_sold = %s WHERE Sales.invoice_id = %s AND Sales.product_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (invoice_id, product_id, quantity_sold, invoice_id, product_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/sales")
        

        

   
    
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 45713))
    app.run(port=port, debug=True)
