#importing libraries
from flask import render_template, request,session,jsonify
from flask.helpers import url_for
from flask.templating import render_template_string
import qrcode
import pandas as pd
from flask import Blueprint
from werkzeug.utils import redirect
from .database import mysql
import datetime
import os
import pyodbc
from .sign import user_details
from .sign import uniqueID

#Blueprint helps to divide the single flask file into various py files 
#creating blueprint for this file with variable
#which will be called in __init__ file

qrcodeFunctions = Blueprint("qrcodeFunctions",__name__,static_folder="static", template_folder="templates")

@qrcodeFunctions.route('/qrcode_info',methods = ['POST','GET'])
def qrcode_info():
    msg=''
    if request.method == 'POST':
        description = request.form['description']
        locationid = request.form['locationid']
        customerid = request.form['customerid']
        batchID = request.form['batchID']
        qrcodeid=uniqueID(locationid)
        cursor = mysql.cursor()
        cursor.execute('''INSERT INTO QRcodeDB(QRcodeID,Description, location,CustomerID,status,batchID,year) VALUES(?,?,?,?,?,?,?)''' ,(qrcodeid,description,locationid,customerid,"unallocated",batchID,datetime.date.today().year))
        mysql.commit()
        cursor.close()
        msg='Data updated'
    return render_template('qrcode_info.html', msg=msg)

@qrcodeFunctions.route('/qrcodeview')
def qrcodeview():
    qrcode_details=[]
    cursor = mysql.cursor()
    cursor.execute('SELECT * from QRcodeDB')
    total_rows = cursor.fetchall()
    cursor.execute('SELECT QRcodeID,Description,location FROM QRcodeDB WHERE status =?',"unallocated")
    qrcode_detail = cursor.fetchall()
    mysql.commit()
    df = pd.DataFrame(qrcode_details)
    for i in range(0,len(qrcode_detail)):
        print(qrcode_detail[i])
        qrcode_img = qrcode.make(data="company:niaagro,QRcodeID: {},Description:{},LocationID:{}".format(qrcode_detail[i][0],qrcode_detail[i][1],qrcode_detail[i][2])) 
        qrcode_img.save(r"C:\Users\Dell\Desktop\Internship\flask and rest api\qrcodes\{}.png".format(qrcode_detail[i][0]))
        img = read_file(r"C:\Users\Dell\Desktop\Internship\flask and rest api\qrcodes\{}.png".format(qrcode_detail[i][0]))
        cursor.execute('UPDATE QRcodeDB SET Status=? WHERE QRcodeID = ? ',"allocated",qrcode_detail[i][0])
        cursor.execute('UPDATE QRcodeDB SET QRimage =? where QRcodeID=? ',(pyodbc.Binary(img),qrcode_detail[i][0]))
        mysql.commit()
        cursor.close()
    print(qrcode_details)
    return render_template("qrcodeview.html")



@qrcodeFunctions.route('/realtimescan',methods = ['POST','GET'])
def realtimescan():
    return render_template("realtimescan.html")


@qrcodeFunctions.route('/qrscanning', methods=['POST','GET'])
def qrscanning():
    out_String=""
    rf=request.get_data()
    data = rf.decode("utf-8")
    qrcodeID,flag = extractor(data)
    if flag==True:
        msg="QrcodeID:"+ str(qrcodeID).strip()
        session['QRcodeID'] = qrcodeID
        user_details()
    else:
        msg = qrcodeID
    out_string = msg
    print(out_string)
    return jsonify(msg)

@qrcodeFunctions.route('/outString',methods=['GET','POST'])
def outString():
    return render_template('outString.html')


def extractor(decoded_string):
    res = decoded_string.split(',')
    data = []
    for i in res:
        d,r = i.split(':')
        data.append((d,r))
    flag= (data[0][1])
    if flag.lower() != 'niaagro':
        msg = "NOT OWNED BY NIAAGRO, things printed on qrcode are :" + decoded_string 
        return msg,False
    else:
        return data[1][1],True


def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo

