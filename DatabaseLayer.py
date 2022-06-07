import mysql.connector
#from flask_mysqldb import mysql

def addNewUser(username,password,email,phone):
    mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="",
                               database="appdb")
    mycursor = mydb.cursor()
    sql ="INSERT INTO `accounts` (`username`, `password`, `email`, `phone`) VALUES ( %s, %s, %s, %s);"
    val = (username,password,email,phone)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

   # print(mycursor.rowcount, "record inserted.")

def LoginChek(username,password):
    mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="",
                               database="appdb")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM accounts WHERE username='"+username+"' and password='"+ password+"'")
    user = mycursor.fetchone()
    mydb.close()

    if user is None :
        return False  
    else:
        return True

#addNewUser("1","1","1","1")
#print(str(LoginChek('1','1')))