import mysql.connector

try:
    db = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWORD, database=DATABASE,
                                 auth_plugin='mysql_native_password')
    mycursor = db.cursor()

    db.commit()
except:

    print("no internet connection from jump")
