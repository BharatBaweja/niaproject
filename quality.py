from flask import render_template, request, session
from flask import Blueprint
from database import mysql
import pyodbc
import os
grainquality = Blueprint("grainquality",__name__,static_folder="static", template_folder="templates")

UPLOAD_FOLDER = 'static/uploads'
@grainquality.route("/quality", methods=['GET', 'POST'])
def quality():
	QRcodeID = session['QRcodeID']
	cursor = mysql.cursor()
	cursor.execute('''SELECT location FROM QRcodeDB where QRcodeID=?''',QRcodeID)
	location= cursor.fetchall()
	location= str(location)
	cursor.execute('''SELECT batchID FROM QRcodeDB where QRcodeID=?''',[QRcodeID])
	batch= cursor.fetchall()
	batch= str(batch)
	mysql.commit()
	cursor.close()
	return render_template("quality.html", qrid=QRcodeID, location= location, batch=batch)

@grainquality.route('/send', methods=['POST'])
def send():
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
	if request.method == 'POST':
		temp = request.form['temp']
		hum = request.form['hum']
		gas = request.form['gas']
		image= request.files['file']
		variety= request.form['variety']
		filename = image.filename
		image.save(os.path.join(UPLOAD_FOLDER, filename))
		img = read_file(r"C:\Users\Dell\Desktop\Internship\flask and rest api\static\uploads\{}".format(filename))
		if variety == 'wheat':
			if float(temp)>=15 and float(temp)<=35 and float(hum)>=20 and float(hum)<=39 and float(gas)>=0 and float(gas)<=500:
				grade="Good"
			elif float(temp)>=36 and float(temp)<=45 and float(hum)>=40 and float(hum)<=50 and float(gas)>=501 and float(gas)<=1000:
				grade="Critical"
			elif float(temp)>=46 and float(temp)<=75 and float(hum)>=51 and float(hum)<=100 and float(gas)>=1001 and float(gas)<=2000:
				grade="Risk"
			else:
				grade="Risk"
			cursor = mysql.cursor()
		
			cursor.execute("INSERT INTO QualityDB(QRcodeID,Temperature,Humidity,Co2GasConcentration,TypeCategory1,QualityGrade,Image) VALUES(?,?,?,?,?,?,?)",(QRcodeID,temp,hum,gas,variety,grade,pyodbc.Binary(img)))

			mysql.commit()
			cursor.close()
			return render_template('quality.html', grade=grade, qrid=QRcodeID, temp=temp, hum=hum, gas=gas, variety=variety)
		elif variety == 'paddy':
			if float(temp)>=22 and float(temp)<=30 and float(hum)>=50 and float(hum)<=70 and float(gas)>=0 and float(gas)<=500:
				grade="Good"
			elif float(temp)>=31 and float(temp)<=35 and float(hum)>=71 and float(hum)<=80 and float(gas)>=501 and float(gas)<=1000:
				grade="Critical"
			elif float(temp)>=36 and float(temp)<=65 and float(hum)>=81 and float(hum)<=100 and float(gas)>=1001 and float(gas)<=2000:
				grade="Risk"
			else:
				grade="Risk"
			cursor = mysql.cursor()
			cursor.execute("INSERT INTO QualityDB(QRcodeID,Temperature,Humidity,Co2GasConcentration,TypeCategory1,QualityGrade,Image) VALUES(?,?,?,?,?,?,?)",(QRcodeID,temp,hum,gas,variety,grade,pyodbc.Binary(img)))
			mysql.commit()
			cursor.close()
			return render_template('quality.html', grade=grade, qrid=QRcodeID, temp=temp, hum=hum, gas=gas, variety=variety)
		elif variety == 'maize':
			if float(temp)>=5 and float(temp)<=30 and float(hum)>=18 and float(hum)<=30 and float(gas)>=0 and float(gas)<=500:
				grade="Good"
			elif float(temp)>=31 and float(temp)<=40 and float(hum)>=31 and float(hum)<=35 and float(gas)>=501 and float(gas)<=1000:
				grade="Critical"
			elif float(temp)>=41 and float(temp)<=65 and float(hum)>=36 and float(hum)<=100 and float(gas)>=1001 and float(gas)<=2000:
				grade="Risk"
			else:
				grade="Risk"
			cursor = mysql.cursor()
			cursor.execute("INSERT INTO QualityDB(QRcodeID,Temperature,Humidity,Co2GasConcentration,TypeCategory1,QualityGrade,Image) VALUES(?,?,?,?,?,?,?)",(QRcodeID,temp,hum,gas,variety,grade,pyodbc.Binary(img)))
			mysql.commit()
			cursor.close()
			return render_template('quality.html', grade=grade, qrid=QRcodeID, temp=temp, hum=hum, gas=gas, variety=variety)
		elif variety == 'soya':
			if float(temp)>=20 and float(temp)<=35 and float(hum)>=10 and float(hum)<=15 and float(gas)>=0 and float(gas)<=500:
				grade="Good"
			elif float(temp)>=36 and float(temp)<=45 and float(hum)>=16 and float(hum)<=20 and float(gas)>=501 and float(gas)<=1000:
				grade="Critical"
			elif float(temp)>=46 and float(temp)<=65 and float(hum)>=21 and float(hum)<=100 and float(gas)>=1001 and float(gas)<=2000:
				grade="Risk"
			else:
				grade="Risk"
			cursor = mysql.cursor()
			print("Sending image to database")
			cursor.execute("INSERT INTO QualityDB(QRcodeID,Temperature,Humidity,Co2GasConcentration,TypeCategory1,QualityGrade,Image) VALUES(?,?,?,?,?,?,?)",(QRcodeID,temp,hum,gas,variety,grade,pyodbc.Binary(img)))
			mysql.commit()
			cursor.close()
			return render_template('quality.html', grade=grade, qrid=QRcodeID, temp=temp, hum=hum, gas=gas, variety=variety, location= location, batch = batch)

		else:
			return render_template('quality.html',qrid=QRcodeID, location= location, batch = batch)

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo
