#IMPORTING REQUIRED LIBRARIES AND OTHER FILES

from flask import Flask,render_template
from qrcodeFunctions import qrcodeFunctions
from sign import sign
from extract import extract
from grainrecognitionapp import grainrecognition
from quality import grainquality
from manualquality import manualquality
#INITIATE A FLASK APP, REGISTER BLUEPRINT IS CALLING THE OTHER PY FILES
def create_app():
    app = Flask(__name__)
    app.secret_key = "NiaAgro"
    app.register_blueprint(qrcodeFunctions) # contains all the qrcode functions
    app.register_blueprint(sign) # contains login/logout, register and admin panel
    app.register_blueprint(extract) # contains function to extract the details of qrcode and product
    app.register_blueprint(grainrecognition)
    app.register_blueprint(grainquality)
    app.register_blueprint(manualquality)
    return app
app = create_app() 

#welcome page for the application
@app.route('/')
def welcomepage():
  return render_template('welcome.html')  

if __name__=="__main__":
  #mymodel= load_model_from_file()
  app.run(debug=True)

