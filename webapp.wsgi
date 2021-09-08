import sys

sys.path.insert(0,'/var/www/webApp/')

from webApp import app as application
application.secret_key = "Nia-Agro"
