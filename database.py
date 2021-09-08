import pyodbc
server = 'niaagro.database.windows.net'
database = 'NiaAgro'
username = 'niaagro'
password = 'Agro@123456'   
driver='{ODBC Driver 17 for SQL Server}'
mysql = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
