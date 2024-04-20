# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:55:16 2021

@author: rmore
"""

import os  
import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  QTime, QDate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation, QRect, QThread

from PyQt5.QtGui import QPixmap, QIcon

import xlrd
from bs4 import BeautifulSoup
import requests

from Mapping_Progress.progressBar_class import progressBar
from definitions_Worker_class import worker_Definitions


class MainGUI(QDialog):
    def __init__(self):

        
        super().__init__() 
        
        # IMPORTAR EL ARCHIVO .ui -------------------------------------------- 
        uic.loadUi('pasapalabra_MainGUI.ui', self)
        
        # ADD LOGOS
        folder_Icon = QIcon('folder_incon_white.png')
        load_Icon = QIcon('load_Icon_white.png')
        clear_Icon = QIcon('clear_Icon.png')
        generate_Icon = QIcon('mapping_Icon.png')
        menu_Icon = QIcon('menu_Icon.png')
        
        self.menu_btn.setIcon(menu_Icon)
        self.search_File_btn.setIcon(folder_Icon)
        self.file_load_btn.setIcon(load_Icon)
        self.pb_clear_log.setIcon(clear_Icon)
        self.create_File_btn.setIcon(generate_Icon)
        self.getWords_btn.setIcon(load_Icon)
        
        # ATRIBUTOS DE CLASE
        self.excelFile = '' # String con la ruta del archivo csv selccionado por el usuario
        self.cursor = self.pt_log.textCursor()
        self.cursor.setPosition(0)
        
        
        # CONEXIONES CON LOS BOTONES
        self.search_File_btn.clicked.connect( self.selectFile )
        self.file_load_btn.clicked.connect( self.loadFile )
        self.getWords_btn.clicked.connect( self.getWords )
        self.create_File_btn.clicked.connect( self.createFile )
        
    def time( self ):
        try:
            hora_actual = QTime.currentTime( )
            return hora_actual.toString( "hh:mm:ss" )
        except:
            return 'no-time' 
        
    def EscribirLog( self, message ):
        
        self.pt_log.setTextCursor(self.cursor) # Poner el cursor del Log en la posición donde ha acabado el último mensaje
        self.pt_log.insertPlainText(  self.time(  ) + message + '\n' )
        self.cursor = self.pt_log.textCursor() # Guardar la posición siguiente donde seguir escribiendo, donde ha acabado el último mensaje    
        
    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName( self, 'Open file...', '', 'xlsx (*.xlsx);; xlsm (*.xlsm) ' )
        
        if( fname != None and fname != '' ):
            self.excelFile = fname
            self.file_Selected_Line.setText ( fname ) # Escribo la ruta del csv seleccionado por el usuario en la línea de texto correspondiente
        
    def loadFile(self):
        
        self.book = xlrd.open_workbook(self.excelFile) # Abrir el archivo excel
        
        self.sheet_Number = self.book.nsheets # Número de hojas del excel
        self.sheet_Names = self.book.sheet_names() # Lista con los nombres de las hojas del archivo excel (strings)
        
        self.EscribirLog( ' Libro de excel abierto. {0} hojas detectadas.'.format(self.sheet_Number) )
        
        
        # print("The number of worksheets is", self.sheet_Number)
        # print("Worksheet name(s): ", self.sheet_Names) # [Hoja1, Hoja2]
        self.sheet_Names.extend(['all'])
        
        
        self.excelSheets_comboBox.addItems(self.sheet_Names)
        
        self.file_load_Status.setText( 'Loaded' )
        self.file_load_Status.setStyleSheet('color:green')
        
    def getWords(self):
        
        
        self.sheet_Selection = self.excelSheets_comboBox.currentText() # Guardo la hoja del excel seleccionada por el usuario en el combo box
        
        # CALCULAR EL NÚMERO DE FILAS Y COLUMNAS DE LAS HOJAS SELECCIONADAS
        if (self.sheet_Selection != 'all'):
            self.selected_Sheet = self.book.sheet_by_name(self.sheet_Selection)
            self.nRows = self.selected_Sheet.nrows # Número de filas de la hoja
            self.nCols = self.selected_Sheet.ncols # Número de columnas de la hoja
         
        else:
            
            self.nRows = {} # Diccionario de tipo --> 'Hoja1': Número de filas de la Hoja1
            self.nCols = {} # Diccionario de tipo --> 'Hoja1': Número de columnas de la Hoja1
            
            
            for sheet in self.sheet_Names: # 'Hoja1'
                if sheet != 'all':
                    
                    self.selected_Sheet = self.book.sheet_by_name(sheet)
                    self.nRows[sheet] = self.selected_Sheet.nrows  # Número de filas de la hoja
                    self.nCols[sheet] = self.selected_Sheet.ncols  # Número de columnas de la hoja
                else:
                    continue
            
        
        # print('Número de filas', self.nRows)
        # print('Número de columnas', self.nCols)
        
        # OBTENER EL CONTENIDO DE LAS CELDAS
        self.words = []
        if (self.sheet_Selection != 'all'):
            for col in range(self.nCols):
                for row in range(self.nRows):
                    if self.selected_Sheet.cell_value(row,col) != '':
                        if self.selected_Sheet.cell_value(row,col) in self.words: # Si la palabra está repetida me salto la iteración
                            continue
                        else:
                            self.words.extend( [self.selected_Sheet.cell_value(row,col)] )
                    else:
                        continue
                    
        else: # all sheets
            for sheet in self.sheet_Names: # 'Hoja1'
                if sheet != 'all':
                    
                    col = 0
                    row = 0
                    self.selected_Sheet = self.book.sheet_by_name(sheet)
                    for col in range(self.nCols[sheet]):
                        for row in range(self.nRows[sheet]):
                            if self.selected_Sheet.cell_value(row,col) != '':
                                if self.selected_Sheet.cell_value(row,col) in self.words: # Si la palabra está repetida me salto la iteración
                                    continue
                                else:
                                    self.words.extend( [self.selected_Sheet.cell_value(row,col)] )
                            else:
                                continue
                    
                else:
                    continue
        
        self.words = [x.lower() for x in self.words]
        self.words.sort(key = lambda p: p.lower().replace('á', 'a'). \
                        replace('é', 'e').replace('í','i'). \
                        replace('ó','o').replace('ú','u')) # Ordenar las palabras alfabéticamente
        print(self.words[:20])
        
        self.words_load_Status.setText( 'Loaded' )
        self.words_load_Status.setStyleSheet('color:green')
        
        self.EscribirLog( ' Se han obtenido {0} palabras.'.format(len(self.words)) )
            
    def createFile(self):
        if self.file_load_Status.text(  ) != 'Loaded':
            self.EscribirLog( ' Se necesita cargar un archivo' )
            return
        if self.words_load_Status.text(  ) != 'Loaded':
            self.EscribirLog( ' Se necesita obtener la infomación del archivo' )
            return
        
        msgbox = QMessageBox()
        msgbox.setWindowTitle('Generar archivo')
        msgbox.setText('¿Desea generar el archivo?')
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No )
        
        
        reply = msgbox.exec()
        
        if reply == QMessageBox.Yes:
            
            
            
            directory, _ = QFileDialog.getSaveFileName(self, 'Save project', '', 'txt (*.txt)' )
            
            self.configdir = directory
            
            # output = open(self.configdir, "w")
            
            # Instancio la clase de la barra de progreso circular     
            self.myProgressBar = progressBar()    
            self.myProgressBar.show()
            self.myProgressBar.progressBarValue(0) # Al principio los nodos mapeados son un 0%
            
            # Instancio el thread correspondiente al mapeo
            # Step 2: Create a QThread object
            self.thread = QThread()
            
            # Step 3: Create a worker object
            self.worker = worker_Definitions(self.configdir, self.words)
            
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.myProgressBar.close) # Al terminar el mapeo se cierra la barra de progreso
            
            # Step 6: Start the thread
            self.thread.start()
            
            self.worker.progress.connect( self.update_Progress )
            self.worker.messagesToLog.connect( self.wrtiteLogFromExternal )
            
            
            
            
            
            
            # for word in self.words:                
            #     output.write(word + ': \n')  
            #     definition = self.searchDefinition(word)                
            #     output.write(definition)
            #     output.write('\n \n')
                
            # output.close()
            
            #self.EscribirLog( ' Archivo de texto creado' )
            
    def searchDefinition(self, word):
        
        source = requests.get('https://www.wordreference.com/definicion/' + word).text # Se busca la dirección web
        soup = BeautifulSoup(source, 'lxml')
        
        try:
        
            section = soup.find('ol')
            
            
            definition = section.li.text
            
            definition = definition.strip() # Eliminar los espacios en blanco del principio y del final
            
            
            # Hay veces que en wordReference pone un ejemplo con la palabra detrás de dos puntos. Esta frase ejemplo la quiero quitar
            if definition.find(':') != -1:
                definition = definition.split(':')[0]
                
            if definition[ len(definition) - 1] != '.':
                definition = definition + '.'
                
            
            
        except AttributeError:
            definition = 'Definición no encontrada'
        
       
        
        return definition
    
    @pyqtSlot(float, int)
    def update_Progress(self, progress_Value, iteration):
        
        self.myProgressBar.progressBarValue(iteration * progress_Value)
        QApplication.processEvents()
        
    @pyqtSlot(str)
    def wrtiteLogFromExternal(self, mes):
        self.EscribirLog(mes)
        
        
def main():
    
    app  = QApplication(sys.argv)
    myGUI = MainGUI()
    myGUI.show()    
    
    try:
        sys.exit(app.exec_())
        
    except:
        print('Exiting')
   

if __name__ == "__main__":
    main()