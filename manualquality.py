from flask import render_template, request,session
from flask import Blueprint
from .database import mysql
import pyodbc
import os
manualquality = Blueprint("manualquality",__name__,static_folder="static", template_folder="templates")

UPLOAD_FOLDER = 'static/uploads'
@manualquality.route("/manquality", methods=['GET', 'POST'])
def manquality():
	QRcodeID = session['QRcodeID']
	cursor = mysql.cursor()
	cursor.execute('''SELECT location FROM QRcodeDB where QRcodeID=?''',[QRcodeID])
	location= cursor.fetchall()
	location= str(location)
	cursor.execute('''SELECT batchID FROM QRcodeDB where QRcodeID=?''',[QRcodeID])
	batch= cursor.fetchall()
	batch= str(batch)
	mysql.commit()
	cursor.close()
	return render_template("manquality.html", qrid=QRcodeID, location= location, batch=batch)

@manualquality.route('/mansend', methods=['POST','GET'])
def mansend():
	if request.method == 'POST':
		temp = request.form['parameter1']
		hum = request.form['parameter2']
		gas = request.form['parameter3']
		image= request.files['file']
		variety= request.form['variety']
		grade= request.form['quality']
		QRcodeID = session['QRcodeID']
		filename = image.filename
		image.save(os.path.join(UPLOAD_FOLDER, filename))
		img = read_file(r"C:\Users\Dell\Desktop\Internship\flask and rest api\static\uploads\{}".format(filename))
		cursor = mysql.cursor()
		cursor.execute('''SELECT location FROM QRcodeDB where QRcodeID=?''',[QRcodeID])
		location= cursor.fetchall()
		location= str(location)
		cursor.execute('''SELECT batchID FROM QRcodeDB where QRcodeID=?''',[QRcodeID])
		batch= cursor.fetchall()
		batch= str(batch)
		cursor.execute("INSERT INTO QualityDB(QRcodeID,Temperature,Humidity,Co2GasConcentration,TypeCategory1,QualityGrade,Image) VALUES(?,?,?,?,?,?,?)",(QRcodeID,temp,hum,gas,variety,grade,pyodbc.Binary(img)))
		mysql.commit()
		return render_template('manquality.html', grade=grade, qrid=QRcodeID, temp=temp, hum=hum, gas=gas, variety=variety)
	return render_template('manquality.html')


def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo
