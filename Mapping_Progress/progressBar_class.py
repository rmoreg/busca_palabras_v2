# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:14:14 2021

@author: rmore
"""

import sys
import re
import math
import numpy as np
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QTableWidgetItem, QListWidget, QListWidgetItem, QStyledItemDelegate
from PyQt5.QtWidgets import QMessageBox, QFrame
from PyQt5.QtCore import  QTime, QDate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation, QRect, QThread

from PyQt5.QtGui import QPixmap, QIcon

import time



class progressBar(QDialog):
    def __init__(self):

        
        super().__init__() 
        
        # IMPORTAR EL ARCHIVO .ui -------------------------------------------- 
        uic.loadUi('roundProgressBar.ui', self)

        # Remove Title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            

    # DEF PROGRESS BAR VALUE
    def progressBarValue(self, value):
        
        # PROGRESS BAR STYLESHEET BASE
        styleSheet = """
        
        QFrame{	
        	border-radius: 105.49px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(0, 85, 255, 255));
        }        
        """
        
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUE
        # Stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0 # Progreso que queda
        
        
        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        
        # SET VALUES TO NEW STYLESHEET
        newStyleSheet = styleSheet.replace( '{STOP_1}', stop_1 ).replace( '{STOP_2}', stop_2 )
        
        # APPLY STYLESHEET WITH VALUES
        self.circularProgress.setStyleSheet(newStyleSheet)
        
        # TEXT PERCENTAGE
        htmlText = """<html><head/><body><p><span style=" font-weight:600;">{VALUE}%</span></p></body></html>"""
        
        # REPLACE VALUE
        newHtml = htmlText.replace( '{VALUE}', str(int(value)) )
        
        # APPLY NEW PERCENTAGE TEXT
        self.label_progress.setText(newHtml)
        
        





if __name__ == "__main__":
    
    app  = QApplication(sys.argv)
    myProgressBar = progressBar()    
    myProgressBar.show() 
    
    for i in range(101):
        myProgressBar.progressBarValue(i)
        time.sleep(0.1)
        QApplication.processEvents()
        
    
    try:
        sys.exit(app.exec_())
        
    except:
        print('Exiting')
        
        
       