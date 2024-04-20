# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:30:56 2021

@author: rmore
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import xlrd
from bs4 import BeautifulSoup
import requests

class worker_Definitions(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal(float, int)
    messagesToLog = pyqtSignal(str)
    
    
    def __init__(self, file_Path, words_List):                
        super().__init__()
        self.file_Path = file_Path
        self.words_List = words_List
        
        
    def run(self): # BUSCAR DEFINICIONES
    
        total_Words = len(self.words_List)
        progress_Step = 100.0/total_Words # Porcentaje con respecto al total que representa una palabra. Cada vez que se obtienen la definición de una palabra se avanzará este porcentaje en la barra de progreso.
        
        output = open(self.file_Path, "w")
        
        i = 0
        for word in self.words_List:
                            
              
            definition = self.searchDefinition(word) 

            try:
                if definition != 'Definición no encontrada':
                    output.write(word + ': \n')
                    output.write(definition)
                    output.write('\n \n')
                else:
                    print(word)
                    
                
            except UnicodeEncodeError:
                print('caracter extraño en la definición de la palabra', word)
            
            
            self.progress.emit(progress_Step, i + 1) # Emito el porcentaje que corresponde a la iteración i completada
            i+=1
        
        output.close()
        self.finished.emit()
        self.messagesToLog.emit(" Archivo de texto creado.")
        
        
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
                
            if definition.find('♦') != -1: # Si se encuentra ese caracter especial lo tego que quitar para poder escribirlo en el archivo de texto
                definition = definition.split('♦')[0]
                
            
            
        except AttributeError:
            definition = 'Definición no encontrada'
            
        
        
       
        
        return definition