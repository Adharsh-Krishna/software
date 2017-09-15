from PyQt4.Qt import *
from PyQt4 import QtGui
import os
import sys


def message_alert(text_data,info_data,title,detailed_data):
	msg= QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text_data)
        msg.setInformativeText(info_data)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailed_data)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(msgbtn)
        msg.exec_()


def msgbtn(i):
	print "Button pressed is:",i.text()
