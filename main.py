from mailing import *
import smtplib
from PyQt4.Qt import *
from PyQt4 import QtGui
import os
import ui
import sys
from pymongo import MongoClient 
import pprint  
import passwordmeter
import random
from validate_email import validate_email
from aes import *
import hashlib
from mongo import *
from app_utils import *
import os.path


client = MongoClient()  
db=client.software
userdetails=db.user_details

class mainapp(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self,parent=None):
		super(mainapp,self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.login_execute)
		self.pushButton_3.clicked.connect(self.register_execute)
		self.pushButton_6.clicked.connect(self.recovery_execute)
		self.pushButton_5.clicked.connect(self.checkanswer_execute)
		self.pushButton_4.clicked.connect(self.confirmcode_execute)
		self.pushButton_7.clicked.connect(self.file_explorer_execute1)
		self.pushButton_8.clicked.connect(self.directory_explorer_execute1)
		self.pushButton_2.clicked.connect(self.encrypt_file)
		self.pushButton_9.clicked.connect(self.hide_file)
		self.pushButton_15.clicked.connect(self.file_explorer_execute2)
		self.pushButton_24.clicked.connect(self.directory_explorer_execute2)
		self.pushButton_26.clicked.connect(self.decrypt_file)
		self.pushButton_25.clicked.connect(self.show_hidden)
		self.pushButton_27.clicked.connect(self.directory_explorer_execute3)
		self.pushButton_32.clicked.connect(self.unhide_file)
		self.pushButton_30.clicked.connect(self.change_fullname)
		self.pushButton_31.clicked.connect(self.change_password)
		self.pushButton_44.clicked.connect(self.change_phone)
		self.pushButton_45.clicked.connect(self.change_email)
		self.pushButton_29.clicked.connect(self.send_email)
		self.pushButton_28.clicked.connect(self.file_explorer_execute3)
		self.pushButton_46.clicked.connect(self.show_history)
		self.pushButton_47.clicked.connect(self.clear_history)


	def show_history(self):
		db_name=str(self.lineEdit.text())
		client=MongoClient()
		db=client[db_name]
		history=db.history
		all_history=history.find({})
		data1=""
		data2=""
		for entry_t in all_history:
			data1=data1+str(entry_t['_id'].generation_time)+"\n"
			data2=data2+str(entry_t['content'])+"\n"
		print data2
		self.textEdit_2.setText(data1)
		self.textEdit_17.setText(data2)

	def clear_history(self):
		db_name=str(self.lineEdit.text())
		client=MongoClient()
		db=client[db_name]
		history=db.history
		history.drop()
		message_alert("Successful","History cleared permanently","Alert","The details are as follows:")

	def send_email(self):
		db_name=str(self.lineEdit.text())
		sender=str(self.lineEdit_24.text())
		receiver=str(self.lineEdit_25.text())
		subject=str(self.lineEdit_26.text())
		body=str(self.lineEdit_35.text())
		filename=str(self.lineEdit_17.text())
		password=str(self.lineEdit_36.text())
		valid1=validate_email(sender)
		valid2=validate_email(receiver)
		if valid1==True and valid2==True:
			send_mail_attachment(sender,receiver,subject,body,filename,password)
			self.lineEdit_8.setText("Mail sent to "+receiver+" with file :"+filename+" successfully")
			update_history(db_name,"Mail sent to"+receiver+" with file :"+filename+" successfully")
		else:
			self.lineEdit_8.setText("Invalid sender/receiver email ID")
			update_history(db_name,"Unsuccessful: Mail sent to"+receiver+" with file :"+filename+" successfully")

	def change_password(self):
		username=str(self.lineEdit.text())
		old_password=str(self.lineEdit_28.text())
		new_password=str(self.lineEdit_29.text())
		renew_password=str(self.lineEdit_30.text())
		val=userdetails.find_one({"username":username},{"_id":0,"password":1})
		if old_password==str(val['password']):
			
			if new_password!=renew_password:
				message_alert("Password Mismatch","Please enter same password on both the fields","Alert","The details are as follows")
			else:
				pass_strength, pass_improvement=passwordmeter.test(new_password)
				if pass_strength<0.25:
					message_alert("Password strength:weak",pass_improvement['charmix'],"Alert","The details are as follows")
				else:
					userdetails.update_one({"username":username},{"$set":{"password":new_password}})
					message_alert("Password changed successfully","Password changed successfully","Alert","The details are as follows")
					update_history(username,"Password Changed")
		else:
			message_alert("Password Incorrect","Please enter the correct password","Alert","The details are as follows")


	def change_phone(self):
		username=str(self.lineEdit.text())
		changed_phone=str(self.lineEdit_31.text())
		userdetails.update_one({"username":username},{"$set":{"phone":changed_phone}})
		message_alert("Phone Number changed successfully","Phone Number changed to "+changed_phone,"Alert","The details are as follows")
		update_history(username,"Phone NUmber Changed to "+changed_phone)


	def change_email(self):
		username=str(self.lineEdit.text())
		changed_email=str(self.lineEdit_45.text())
		valid=validate_email(changed_email)
		if valid==True:
			userdetails.update_one({"username":username},{"$set":{"email":changed_email}})
			message_alert("E-mail changed successfully","E-mail changed to "+changed_email,"Alert","The details are as follows")
			update_history(username,"Email changed to "+changed_email)
		else :
			message_alert("E-mail change unsuccessful","Enter a valid email","Alert","The details are as follows")



	def change_fullname(self):
		username=str(self.lineEdit.text())
		changed_fullname=str(self.lineEdit_27.text())
		userdetails.update_one({"username":username},{"$set":{"fullname":changed_fullname}})
		message_alert("Full Name changed successfully","Full Name changed to "+changed_fullname,"Alert","The details are as follows")
		update_history(username,"Full Name changed to "+changed_fullname)


	def show_hidden(self):
		db_name=str(self.lineEdit.text())
		client=MongoClient()
		db=client[db_name]
		hidden=db.hidden_files
		all_files=hidden.find({})
		data="FILENAME       "+"DATE    "+"   TIME "+"\n"
		for doc in all_files:
			data=data+ str(doc['filename']) +" "+ str(doc['_id'].generation_time)
			data=data+"\n"
		self.textEdit.setText(data)	
		

	def unhide_file(self):
		file_name=str(self.lineEdit_34.text())
		target_folder=str(self.lineEdit_22.text())
		password=str(self.lineEdit_23.text())
		db_name=str(self.lineEdit.text())
		des=unhide_encrypted_file(db_name,file_name,password,target_folder)
		self.lcdNumber_2.display(int(des))
		if os.path.exists(target_folder+"/"+file_name+".enc"):
			message_alert("Successful : File Unhidden","File moved to location : "+target_folder,"Alert","The details are as follows:")
			update_history(db_name,"File:"+file_name+" Unhidden to location"+target_folder)
		else :
			message_alert("Unsuccessful : File Unhidden","Please check the password you entered","Alert","The details are as follows:")
			update_history(db_name,"Unsuccessful File unlock attempt")
			
			
		
	def encrypt_file(self):
		db_name=str(self.lineEdit.text())
		source_file=str(self.lineEdit_15.text())
		target_folder=str(self.lineEdit_16.text())
		enc_type=str(self.comboBox_3.currentText())
		print enc_type
		password=str(self.lineEdit_11.text())
		repassword=str(self.lineEdit_12.text())
		if password==repassword:
			pass_strength, pass_improvement=passwordmeter.test(password)
			if pass_strength<0.25:
				message_alert("Password stregth: weak",pass_improvement['charmix'],"Alert","The details are as follows:")
				
			else :
				
				key=hashlib.sha256(password).digest()
				encrypt_file(key,source_file,target_folder)
				temp="File encrypted and stored at location : "+target_folder
				message_alert("Successfully encrypted",temp,"Alert","The details are as follows:")
				update_history(db_name,"File : "+source_file+" encrypted to location :"+target_folder )
		else:
			 message_alert("Password mismatch","Please enter the same password in both the fields.","Alert","The details are as follows:")			
			 
	def decrypt_file(self):
		db_name=str(self.lineEdit.text())
		source_file=str(self.lineEdit_32.text())
		target_folder=str(self.lineEdit_33.text())
		enc_type=str(self.comboBox_4.currentText())
		password=str(self.lineEdit_21.text())
		user_name=str(self.lineEdit.text())
		key=hashlib.sha256(password).digest()
		decrypt_file(key, source_file,target_folder)
		if os.path.exists(source_file):
			message_alert("File Decryption unsuccessful","Please check the password you entered","Alert","The details are as follows:")
			update_history(db_name,"File : "+source_file+" decrypted to location :"+target_folder )
		else :
			message_alert("File Decrypted","Successfully decrypted file to location :"+target_folder,"Alert","The details are as follows:")
			

	def hide_file(self):
		if self.checkBox.isChecked():
			source_file=str(self.lineEdit_15.text())
        	        target_folder=str(self.lineEdit_16.text())
                	enc_type=str(self.comboBox_3.currentText())
                	password=str(self.lineEdit_11.text())
                	repassword=str(self.lineEdit_12.text())
			destruct_value=str(self.spinBox.value())
			db_name=str(self.lineEdit.text())
			slash_index=source_file.rfind("/")
			file_name=target_folder+"/"+source_file[slash_index+1:]+".enc"
			if not os.path.exists(file_name):
				message_alert("Cannot hide file","Please check the file location","Alert","The details are as follows:")	
			else:			
				hide_encrypted_file(db_name,file_name,enc_type,password,destruct_value)
				update_history(db_name,"File:"+source_file+" hidden")
				message_alert("File hidden","File:"+source_file+" hidden","Alert","The details are as follows:")	
		else:
			message_alert("Cannot hide file","Please check the hide file option to encrypt the file","Alert","The details are as follows:")		

			update_history(db_name,"Unsuccessful File:"+source_file+" lock attempt.")
			

	def file_explorer_execute1(self):
		dlg=QFileDialog()
	        dlg.setFileMode(QFileDialog.AnyFile)
      		filenames = QStringList()
		if dlg.exec_():
			filenames=dlg.selectedFiles()
			f=open(filenames[0],'r')
			with f:
				data=filenames[0]
				self.lineEdit_15.setText(data)

	def file_explorer_execute2(self):
		dlg=QFileDialog()
	        dlg.setFileMode(QFileDialog.AnyFile)
      		filenames = QStringList()
		if dlg.exec_():
			filenames=dlg.selectedFiles()
			f=open(filenames[0],'r')
			with f:
				data=filenames[0]
				self.lineEdit_32.setText(data)


	def file_explorer_execute3(self):
		dlg=QFileDialog()
	        dlg.setFileMode(QFileDialog.AnyFile)
      		filenames = QStringList()
		if dlg.exec_():
			filenames=dlg.selectedFiles()
			f=open(filenames[0],'r')
			with f:
				data=filenames[0]
				self.lineEdit_17.setText(data)

	def directory_explorer_execute1(self):
		dialog= QtGui.QFileDialog()
     		folder_path = dialog.getExistingDirectory(None, "Select Folder")
		self.lineEdit_16.setText(folder_path)

	def directory_explorer_execute2(self):
		dialog= QtGui.QFileDialog()
     		folder_path = dialog.getExistingDirectory(None, "Select Folder")
		self.lineEdit_33.setText(folder_path)

	def directory_explorer_execute3(self):
		dialog= QtGui.QFileDialog()
     		folder_path = dialog.getExistingDirectory(None, "Select Folder")
		self.lineEdit_22.setText(folder_path)

	def login_execute(self):
		username=str(self.lineEdit.text())
		password=str(self.lineEdit_2.text())
		print username
		print password
		userexist_flag=userdetails.find({"username":username}).count()
                if userexist_flag==0 :
			 message_alert("User does not exists","Please login with an existing username","Alert","The details are as follows:")		
                        
		elif userexist_flag>0:
			 userlogin_flag=userdetails.find({"username":username,"password":password}).count()
			 if userlogin_flag==1:
				message_alert("Access Granted","Logging in...","Alert","The details are as follows:")	
				update_history(username,username+"logged in")	
				self.stackedWidget.setCurrentIndex(1)
				creds=userdetails.find_one({"username":username})
				self.lineEdit_27.setText(str(creds['fullname']))
				self.lineEdit_31.setText(str(creds['phone']))
				self.lineEdit_45.setText(str(creds['email']))
				self.lineEdit_24.setText(str(creds['email']))
			 else :
				 message_alert("Incorrect Password","Please enter a valid password for the entered username","Alert","The details are as follows:")		
				 update_history(username,"Unsuccessful login attempt")



	def register_execute(self):
		fullname=str(self.lineEdit_7.text())
		username=str(self.lineEdit_3.text())
		password=str(self.lineEdit_4.text())
		repassword=str(self.lineEdit_5.text())
		email=str(self.lineEdit_8.text())
		phonenumber=str(self.lineEdit_6.text())
		print password
		print repassword
		email_validate=validate_email(email)
		if email_validate==False:
		    message_alert("Invalid Email entered","Please enter a valid email .","Alert","The details are as follows:")	
		   
		if password!=repassword :
		    message_alert("Password Mismatch","Please ensure that the entered password is the same of both the fields","Alert","The details are as follows:")	
                   
		if password==repassword :
		    pass_strength, pass_improvement=passwordmeter.test(password)
                    userexist_flag=userdetails.find({"username":username}).count()
		    if userexist_flag>0 :
			  message_alert("User already exists","Please login with an existing user name or create a new user ","Alert","The details are as follows:")
                         

		    elif pass_strength<0.25 :
			 message_alert("Password Strength: Low",pass_improvement['charmix'],"Alert","The details are as follows:")
			 
		    else :
			 user_cred={"fullname":fullname,"username":username,"password":password,"email":email,"phone":phonenumber}
			 user_question,ok =QInputDialog.getText(self,"Account Recovery Question","Please set a question")
			 if ok :
				user_cred['question']=str(user_question)
                         user_answer,ok =QInputDialog.getText(self, "Account Recovery Answer","Enter an appropriate answer to the question previously set")
			 if ok:
                                user_cred['answer']=str(user_answer)
				userdetails.insert(user_cred)
			 	temp="New User "+fullname+" with UserName : "+username+" created."
			        message_alert(temp,"Please login with the new user credentials","Alert","The details are as follows:")
				self.stackedWidget.setCurrentIndex(0)
				self.tabWidget.setCurrentIndex(0)
				db_activate(username)



	def recovery_execute(self) :
		recovery_username=str(self.lineEdit_14.text())
		userexist_flag=userdetails.find({"username":recovery_username}).count()
                if userexist_flag==1:
                        query={"username":recovery_username}
                        projection={"_id":0,"question":1}
                        val=userdetails.find_one(query,projection)
                        self.lineEdit_13.setText(val['question'])
		else :
                         temp="Username "+recovery_username+" does not exist."
		         message_alert(temp,"Please enter a valid username.","Alert","The details are as follows:")
			 
                         
	def checkanswer_execute(self):
		recovery_username=str(self.lineEdit_14.text())
		answer=str(self.lineEdit_10.text())
		query={"username":recovery_username}
                projection={"_id":0,"answer":1}
		val=userdetails.find_one(query,projection)

		if val['answer']==answer:
			 secretcode=random.randint(1,1000000)
			 userdetails.update_one({"username":recovery_username},{"$set":{"code":secretcode}})
			 print secretcode
			 projection={"_id":0,"email":1}
			 value=userdetails.find_one(query,projection)
			 send_code(str(value['email']),"Verification Code","Please enter the code to gain access to your account : ",secretcode)
                         temp="A code has been sent to your registered E-mail ID"
		         message_alert(temp,"Please check your E-mail inbox for the code and enter the code in the field given below","Alert","The details are as follows:")
			

                         
			
		else :
			 message_alert("The answer you entered is incorrect","Enter the correct answer for the question shown.","Alert","The details are as follows:")
			
                         
                       

	def confirmcode_execute(self):
		entered_code=str(self.lineEdit_9.text())
		recovery_username=str(self.lineEdit_14.text())
		query={"username":recovery_username}
		projection={"_id":0,"code":1}
                value=userdetails.find_one(query,projection)
		print value['code']
		print entered_code
		if str(entered_code)==str(value['code']):
			 userdetails.update_one({"username":recovery_username},{"$set":{"code":"0000000000"}})
 			 message_alert("Access Granted","Please change your password. ","Alert","The details are as follows:")
			 creds=userdetails.find_one({"username":recovery_username})
			 self.lineEdit_27.setText(str(creds['fullname']))
			 self.lineEdit_31.setText(str(creds['phone']))
			 self.lineEdit_45.setText(str(creds['email']))
			 self.lineEdit_24.setText(str(creds['email']))
			 self.stackedWidget.setCurrentIndex(1) 
			 self.tabWidget_2.setCurrentIndex(3)
			 update_history(recovery_username,"Successful recovery ")
		else :
 			 message_alert("Incorrect code","Try again. ","Alert","The details are as follows:")
			 update_history(recovery_username,"UnSuccessful recovery attempt")

def msgbtn(i):
	print "Button pressed is:",i.text()
def main():
	app=QtGui.QApplication(sys.argv)
        form=mainapp()
	form.show()
	app.exec_()

if __name__=='__main__':
	main()
