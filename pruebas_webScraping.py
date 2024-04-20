# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:27:02 2021

@author: rmore
"""

from bs4 import BeautifulSoup
import requests

word = 'apostatar'

source = requests.get('https://www.wordreference.com/definicion/' + word).text
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
    print(definition)
    
except AttributeError:
    print('No se ha encontrado la palabra')
