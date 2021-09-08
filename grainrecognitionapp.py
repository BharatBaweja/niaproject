
from flask import Flask, redirect, url_for, render_template, request, flash,session
#from PIL import Image
#import cv2
from .database import mysql
from flask import Blueprint
grainrecognition = Blueprint("grainrecognition",__name__,static_folder="static", template_folder="templates")


#Load operation system library
#import os
#os. environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#website libraries
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

#Load math library
import numpy as np

#Load machine learning libraries
#from tensorflow.keras.preprocessing import image
#from keras.models import load_model
#from keras.backend import set_session
#import tensorflow as tf
#from gevent.pywsgi import WSGIServer
#import imquality.brisque as brisque

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'


# def load_model_from_file():  
#     #Set up the machine learning session
#     mymodel = load_model("Saved_models/DenseNet20101")    
#     return mymodel

#Try to allow only images
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Define the view for the top level page
@grainrecognition.route('/grainrecognition/', methods=['GET', 'POST'])
def upload_file():
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
    #Initial webpage load
    if request.method == 'GET' :
        return render_template('image.html', qrid=QRcodeID, location=location, batch=batch)
    else: # if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser may also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # If it doesn't look like an image file
        if not allowed_file(file.filename):
            flash('I only accept files of type'+str(ALLOWED_EXTENSIONS))
            return redirect(request.url)
        #When the user uploads a file with good parameters
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('grainrecognition.uploaded_file', filename=filename, qrid=QRcodeID, location=location, batch=batch))

def validation(path):
    #img = Image.open(path)
    #score= brisque.score(img)
    #if score<= 40:
    #    return 1
    #else:
    return 0

@grainrecognition.route('/uploads/<filename>', methods=['POST', 'GET'])
def uploaded_file(filename):
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
    #img = cv2.imread(UPLOAD_FOLDER+"/"+filename)
    #img = img/255
    #img=cv2.resize(img,(224, 224))
    #img= np.array(img)
    #img = img.reshape(-1,224,224,3)
    pdict = {0:"Wheat",1:"Maize",2:"Paddy",3:"Soya", 4:"NoClass"}
    ###############################prediction#################################
    #prediction = mymodel.predict(img)
    #pred = np.argmax(prediction[0])
    pred = 1

    image_src = "/"+UPLOAD_FOLDER +"/"+filename
    if validation(UPLOAD_FOLDER+"/"+filename)== 1:
        label= pdict[pred]
        answer = "<div class='col'></div><div class='col text-center'><img width='224' height='224' src='"+image_src+"' class='img-thumbnail' /><h4>Category:"+pdict[pred]+": "+"str(prediction[0,pred]*100)"+"</h4></div><div class='w-100'></div>"
        
    else:
        flash("Please upload another image for better result")
        label= pdict[pred]
        answer = "<div class='col'></div><div class='col text-center'><img width='224' height='224' src='"+image_src+"' class='img-thumbnail' /><h4>Category:"+pdict[pred]+": "+"str(prediction[0,pred]*100)" +"</h4></div><div class='w-100'></div>"   
    results.append(answer)
    cursor = mysql.cursor()
    cursor.execute("UPDATE QualityDB SET TypeCategory1 = ? WHERE QRcodeID=?",(label,QRcodeID))
    mysql.commit()
    cursor.close()
    return render_template('image.html', results=results, qrid=QRcodeID, location=location, batch=batch)

results = []

    

