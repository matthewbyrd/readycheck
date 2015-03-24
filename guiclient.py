#!/usr/bin/env python

"""
Runs a GUI client for ReadyCheck, connecting to a socket server.
"""

#######################################################################################################
#                                                                                                     #
#                                   WELCOME TO THE CLIENT FILE                                        #
#                                                                                                     #
#                                                                                                     #
#######################################################################################################


from PyQt4 import QtCore, QtGui
import pygame # For sounds!
import socket
import thread

host = 'localhost'  # to connect to your own machine
port = 4004

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))



#######################################################################################################
#                                                                                                     #
#                                    THE QT CREATOR OUTPUT                                            #
#                                                                                                     #
#                                                                                                     #
#######################################################################################################

def alert():
    pygame.mixer.init()
    pygame.mixer.music.load("alert.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ReadyCheck(object):
    def setupUi(self, ReadyCheck):
        ReadyCheck.setObjectName(_fromUtf8("ReadyCheck"))
        ReadyCheck.resize(304, 359)
        self.gridLayout = QtGui.QGridLayout(ReadyCheck)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit = QtGui.QLineEdit(ReadyCheck)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(ReadyCheck) ##text browser
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 1, 1, 1, 3)
        self.pushButton = QtGui.QPushButton(ReadyCheck)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 2)
        self.pushButton_2 = QtGui.QPushButton(ReadyCheck)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 3)
        self.hear()  #This is the vital bit that adds my hear function to the Qt stuff
        
#######################################################################################################
#                                                                                                     #
#                                    THE WIDGET FUNCTIONS                                             #
#                                                                                                     #
#######################################################################################################

        self.retranslateUi(ReadyCheck)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.sendy)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit.clear)
        # WHEN USERS PRESS ENTER IN MESSAGE BOX
        #Test to send the message
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.sendy)        
        #Then clear the chat pane
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.lineEdit.clear)
        #Make the send button click
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.pushButton.animateClick)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ready) ##readycheck
        QtCore.QMetaObject.connectSlotsByName(ReadyCheck)
        
    def ready(self):         
        """
        Tells the server the user is ready.
        """
        message = '0000000000000000000'
        message = message.encode()
        s.send(message)

    def updateUi(self):         
        text = unicode(self.lineEdit.text())
        self.textBrowser.append(text)        
            
    def sendy(self):  
        """
        Sends the contents of the chat entry to the server
        """
        message = unicode(self.lineEdit.text())
        message = message.encode()
        # Sending the message:
        s.send(message)

    def retranslateUi(self, ReadyCheck):
        ReadyCheck.setWindowTitle(_translate("ReadyCheck", "ReadyCheck", None))
        self.pushButton.setText(_translate("ReadyCheck", "Send", None))
        self.pushButton_2.setText(_translate("ReadyCheck", "Ready!", None))
        
    def hear(self):
        def loop0():
            while 1:
                msg_received = s.recv(1024)
                if msg_received:
                    msg_received = msg_received.decode()
                    if msg_received.strip() == '--- EVERYONE IS READY! ---':
                        alert()
                    self.textBrowser.append(msg_received)
                    self.textBrowser.moveCursor(QtGui.QTextCursor.End) # Autoscrolls chat window
        thread.start_new_thread(loop0, ())
    
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReadyCheck = QtGui.QWidget()
    ui = Ui_ReadyCheck()
    ui.setupUi(ReadyCheck)
    ReadyCheck.show()
    sys.exit(app.exec_())
    

    

    
    
