import re
from flask import render_template, request, redirect, url_for, session
import pandas as pd
from flask import Blueprint
import random, string
import datetime
from database import mysql


sign = Blueprint("sign",__name__,static_folder="static", template_folder="templates")


@sign.route('/login', methods =['GET', 'POST'])
def login():
    msg=''
    if request.method=='POST' and 'email' in request.form and 'password' in request.form and 'options' in request.form:
        table_name = request.form['options']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.cursor()
        cursor.execute('SELECT * FROM {}DB WHERE EmailAddress = ? AND password = ?'.format(table_name), (email, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id']= account[0]
            session['Name'] = account[1]
            session['role'] = table_name
            msg = 'Logged in successfully! Welcome'
            if table_name == 'Client':
                return render_template('client.html',msg=msg)
            elif table_name == 'Warehouse':
                return render_template('warehouse.html',msg=msg)
            elif table_name == 'Admin':
                return render_template('admin.html',msg=msg)    
        else:
            msg = 'Incorrect username/password !'
    return render_template('login.html',msg=msg)


@sign.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('sign.login'))

@sign.route('/warehouse_register', methods =['GET','POST'])
def warehouse_register():
    msg=""
    if request.method=='POST':
        OwnerCompanyName = request.form['OwnerCompanyName']
        OwnerCompanyAddress = request.form['OwnerCompanyAddress']
        state=request.form['state']
        District = request.form['District']
        locationID = request.form['locationID']
        ContactName = request.form['ContactName']
        ContactNumber = request.form['ContactNumber']
        Contactemail = request.form['Contactemail']
        password = request.form['password']
        warehouseID = uniqueID(state)
        cursor = mysql.cursor()
        cursor.execute('''INSERT INTO WarehouseDB(WarehouseID,OwnerCompanyName,OwnerCompanyAddress,state,District,LocationID,ContactName,mobileNumber,EmailAddress, password) VALUES(?,?,?,?,?,?,?,?,?,?)''' ,warehouseID,OwnerCompanyName,OwnerCompanyAddress,state,District,locationID,ContactName,ContactNumber,Contactemail,password)
        mysql.commit()
        cursor.close()
        msg='registered successfully '
    return render_template('warehouse_register.html', msg=msg)

@sign.route('/client_register', methods = ['POST','GET'])
def client_register():
    msg=""
    if request.method=='POST':
        CompanyName = request.form['CompanyName']
        ContactName = request.form['ContactName']
        ContactNumber = request.form['ContactNumber']
        Contactemail = request.form['Contactemail']
        state=request.form['state']
        pincode = request.form['pinCode']
        city = request.form['city']
        password = request.form['password']
        clientID=uniqueID(state)
        cursor = mysql.cursor()
        cursor.execute('''INSERT INTO ClientDB(clientID,CompanyName,ContactName,mobileNumber,EmailAddress,pinCode,city,state,password) VALUES(?,?,?,?,?,?,?,?,?)''' ,clientID,CompanyName,ContactName,ContactNumber,Contactemail,pincode,city,state,password)
        mysql.commit()
        cursor.close()
        msg='registered successfully '
    return render_template('client_register.html', msg=msg)

def user_details():
    if session['loggedin'] == True:
        cursor = mysql.cursor()
        cursor.execute('INSERT into GBTraceDB(QRcodeID,QRscannerID,DateofReading,Time,ScannerPersonnelRole) values(?,?,?,?,?)',(session['QRcodeID'],session['id'],datetime.date.today(),datetime.datetime.now().time(),session['role']))
        cursor.commit()

@sign.route('/admin',methods = ['POST','GET'])
def admin():
    msg=""
    if request.method=='POST' and 'qrcodeID' in request.form:
        qrcodeid = request.form['qrcodeID']
        cursor = mysql.cursor()
        cursor.execute('''SELECT * FROM GBTraceDB where QRcodeID=?''',[qrcodeid])
        records = cursor.fetchall()
        details = pd.DataFrame(records)
        msg = str(len(details)) + " records found"
        return render_template('adminpanel.html',len = len(details), details = details,msg=msg)
    return render_template('admin.html')



@sign.route('/role',methods = ['POST','GET'])
def role():
    if request.method =="POST" and "options" in request.form:
        options = request.form['options']
        if options=="client":
            return render_template("client_register.html")
        else:
            return render_template("warehouse_register.html")
    return render_template("options.html")


def uniqueID(location):
    location = location.lower()
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + location[:3] + str(datetime.date.today().year)[2:]
    return x
