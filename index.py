from unittest import TestResult, result
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import sys

from click import password_option
from torch import equal
from GUI import *

from PyQt5.uic import loadUiType

from os import path

from DatabaseLayer import LoginChek,addNewUser


from predictor import Predictor

login,_ = loadUiType('GUI/login.ui')
register,_ = loadUiType('GUI/register.ui')
selection,_ = loadUiType('GUI/selection.ui')
selectimage,_ = loadUiType('GUI/selectimage.ui')
finalresultcancer,_ = loadUiType('GUI/finalresultcancer.ui')
finalresultdisease,_ = loadUiType('GUI/finalresultdisease.ui')

class Login(QWidget, login):
    def __init__(self , parent=None):
        super(Login , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
    def Handel_UI(self):
        self.setWindowTitle("Login")
        self.setFixedSize(520,300)
        
    def Handel_Buttoms(self):
        self.btnlogin.clicked.connect(self.Login)
        self.btncancel.clicked.connect(self.close)
        self.btnreg.clicked.connect(self.OpenRegister)
    
    def Login(self):
        username= str(self.leusername.text())
        password= str(self.lepassword.text())
        if username =='' or password == '':
            QMessageBox.warning(self , "خطاً بالبيانات المدخلة" , "يجب دخال اسم المستخدم وكلمة المرور")
        else:
            testUser= LoginChek(username , password)
            if testUser:
                self.OpenSelection()
            else:
                QMessageBox.warning(self , "خطاً بالبيانات المدخلة" , "اسم المستخدم او كلمة المرور غير صحيحة")
    
    def OpenSelection(self):
        self.app = QApplication(sys.argv)
        self.window2 = Selection()
        self.hide()
        self.window2.show()
        self.app.exec_()

    def OpenRegister(self):
        self.app = QApplication(sys.argv)
        self.window2 = Register()
        self.hide()
        self.window2.show()
        self.app.exec_()
       
class Register(QWidget, register):
    def __init__(self , parent=None):
        super(Register , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
    def Handel_UI(self):
        self.setWindowTitle("SignUp")
        self.setFixedSize(515,540)
        
    def Handel_Buttoms(self):
        self.btnback.clicked.connect(self.BLogin)
        self.btncancel_2.clicked.connect(self.close)
        self.btnreg2.clicked.connect(self.Registed)

    def BLogin(self):
        self.app = QApplication(sys.argv)
        self.window2 = Login()
        self.hide()
        self.window2.show()
        self.app.exec_()

    def Registed(self):
        username= str(self.username.text())
        password= str(self.password.text())
        cpassword= str(self.cpassword.text())
        email= str(self.email.text())
        phone=str(self.phone.text())
        if username =='' or password =='' or  cpassword =='' :
            QMessageBox.warning(self , "خطأ فى البيانات" , "يجب ادخال اسم المستخدم وكلمة السر")
        else:
            if password != cpassword:
                QMessageBox.warning(self , "خطا فى الباسورد" , "يجب تاكيد كلمة السر")
            else:
                addNewUser(username,password,email,phone)
                QMessageBox.information(self , "Succes" , "Succes registration")
                self.username.setText('')
                self.password.setText('')
                self.cpassword.setText('')
                self.email.setText('')
                self.phone.setText('')

class Selection(QWidget, selection):
    def __init__(self , parent=None):
        super(Selection , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
    def Handel_UI(self):
        self.setWindowTitle("Selction")
        self.setFixedSize(620,250)
        
    def Handel_Buttoms(self):
        self.btndis.clicked.connect(self.SkinDisease)
        self.btncancer.clicked.connect(self.SkinCancer)

    def SkinDisease(self):
        self.app = QApplication(sys.argv)
        self.window2 = SelectImage(detectionType='Disease')
        self.hide()
        self.window2.show()
        self.app.exec_()

    def SkinCancer(self):
        self.app = QApplication(sys.argv)
        self.window2 = SelectImage(detectionType='cancer')
        self.hide()
        self.window2.show()
        self.app.exec_()

class SelectImage(QWidget, selectimage):
    def __init__(self , parent=None,detectionType='cancer'):
        super(SelectImage , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        self.detectionType=detectionType

    def Handel_UI(self):
        self.setWindowTitle("Select Image")
        self.setFixedSize(800,800)
            
    def Handel_Buttoms(self):
        self.btnBrowse.clicked.connect(self.Browse)
        self.btnback.clicked.connect(self.Back)
        self.btntestdisk.clicked.connect(self.TestDiskImage)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)
        self.btncancel.clicked.connect(self.close)
    
    def Back(self):
        self.app = QApplication(sys.argv)
        self.window2 = Selection()
        self.hide()
        self.window2.show()
        self.app.exec_()

    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def Browse(self):
        save_location = QFileDialog.getOpenFileName()
        print(save_location[0])
        imagePath=save_location[0]
        self.lePath.setText(str(save_location[0]))
        if self.lePath.text() !='':
            self.lb1.setPixmap(QPixmap(imagePath));
        else:
            QMessageBox.warning(self , "Data Error" , "You Must Select The Image File")

    def TestDiskImage(self):
        predictor=Predictor()
        Result = predictor.TestImage(path=self.lePath.text(),modeltype=self.detectionType)
        self.app = QApplication(sys.argv)
        if self.detectionType=='cancer':
            self.window2 = FinalResultCancer(result=Result,imagePath=self.lePath.text())
        else:
            self.window2 = FinalResultDisease(result=Result,imagePath=self.lePath.text())
        self.hide()
        self.window2.show()
        self.app.exec_()

class FinalResultCancer(QWidget, finalresultcancer):
    def __init__(self , parent=None,result=[],imagePath=''):
        super(FinalResultCancer , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
        self.lb_image.setPixmap(QPixmap(imagePath))

        dis= list(result.keys())
        self.d1.setText(str(dis[0]))
        self.d2.setText(str(dis[1]))
        self.d3.setText(str(dis[2]))
        self.d4.setText(str(dis[3]))
        self.d5.setText(str(dis[4])) 

        self.finalresult.setText('The type of skin Cancer disease is " '+str(dis[0])+' "')

        vals= list(result.values())
        self.p1.setText(str(round(vals[0]*100))+"%")
        self.p2.setText(str(round(vals[1]*100))+"%")
        self.p3.setText(str(round(vals[2]*100))+"%")
        self.p4.setText(str(round(vals[3]*100))+"%")
        self.p5.setText(str(round(vals[4]*100))+"%")
        
    def Handel_UI(self):
        self.setWindowTitle("Final Results Report")
        self.setFixedSize(650,800)
        
    def Handel_Buttoms(self):        
        self.pushButton_6.clicked.connect(self.NewTest)
        self.btncancel.clicked.connect(self.close)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)

    def NewTest(self):
        self.app = QApplication(sys.argv)
        self.window2 = SelectImage(detectionType='cancer')
        self.hide()
        self.window2.show()
        self.app.exec_()

    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

class FinalResultDisease(QWidget, finalresultdisease):
    def __init__(self , parent=None,result=[],imagePath=''):
        super(FinalResultDisease , self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttoms()
        
        self.lb_image.setPixmap(QPixmap(imagePath))

        dis= list(result.keys())
        self.d1.setText(str(dis[0]))
        self.d2.setText(str(dis[1]))
        self.d3.setText(str(dis[2]))
        self.d4.setText(str(dis[3])) 

        self.finalresult.setText('The type of skin disease is " '+str(dis[0])+' "')

        vals= list(result.values())
        self.p1.setText(str(round(vals[0]*100))+" %")
        self.p2.setText(str(round(vals[1]*100))+" %")
        self.p3.setText(str(round(vals[2]*100))+" %")
        self.p4.setText(str(round(vals[3]*100))+" %")
        
    def Handel_UI(self):
        self.setWindowTitle("Final Results Report")
        self.setFixedSize(650,800)
        
    def Handel_Buttoms(self):        
        self.pushButton_6.clicked.connect(self.NewTest)
        self.btncancel.clicked.connect(self.close)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)

    def NewTest(self):
        self.app = QApplication(sys.argv)
        self.window2 = SelectImage(detectionType='Disease')
        self.hide()
        self.window2.show()
        self.app.exec_()

    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    try:
            
        app = QApplication(sys.argv)
        window = Login()
        window.show()
        app.exec_()
    except:
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()