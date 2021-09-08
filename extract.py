#IMPORTING REQUIRED LIBRARIES
from flask import render_template, request,jsonify
import pandas as pd
from .database import mysql 
from flask import Blueprint 

#Blueprint helps to divide the single flask file into various py files 
#creating blueprint for this file with variable named extract
#which will be called in __init__ file
extract = Blueprint("extract",__name__,static_folder="static", template_folder="templates")

#function to return sensor and product data from database 
def details(qrcodeid):
    cursor = mysql.cursor() #creating cursor to access db
    cursor.execute('''SELECT * FROM GunnyBagDB where QRcodeID=?''',[qrcodeid]) #query to execute
    #map sensor data with column name and put it in dictionary
    fields = map(lambda x:x[0], cursor.description)
    sensor_details = [dict(zip(fields,row))   for row in cursor.fetchall()]
    # cursor.execute('''SELECT ProductDetail1,ProductDetail2 FROM productdb where QRcodeID=%s''',[qrcodeid])
    # fields = map(lambda x:x[0], cursor.description)
    # product_details = [dict(zip(fields,row))   for row in cursor.fetchall()]
    mysql.commit() #saving the changes
    cursor.close() # closing the cursor
    return jsonify(sensor_details)

#fetch all the data related to product with the help of productID
@extract.route('/productfinder',methods = ['POST','GET'])
def productfinder():
    msg=""
    if request.method=='POST' and 'ProductID' in request.form:
        pid = request.form['ProductID']
        return extract.productdetails(pid)
    return render_template('productfinder.html',msg = msg)


#Maps the rows and columns and return a dataframe
def productdetails(pID):
    cursor = mysql.cursor()
    cursor.execute('''SELECT * FROM GunnyBagDB where ProductID=?''',[pID])
    fields = map(lambda x:x[0], cursor.description)
    sensor_details = [dict(zip(fields,row)) for row in cursor.fetchall()]
    mysql.commit()
    cursor.close()
    df = pd.DataFrame(sensor_details)
    table = df.to_html()
    return render_template("details.html",table = table)
