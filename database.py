import mysql.connector

try:
    db = mysql.connector.connect(host="sql3.freesqldatabase.com", user="sql3440599", passwd="cU1kAzDUbq", database="sql3440599",
                                 auth_plugin='mysql_native_password')
    mycursor = db.cursor()

    db.commit()
except:

    print("no internet connection from jump")
