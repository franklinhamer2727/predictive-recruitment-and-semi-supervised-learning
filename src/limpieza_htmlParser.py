from html.parser import HTMLParser
from calendar import c
import re
import numpy as np
import matplotlib.pyplot as plt



ficher = open('html_limpio/23.html','r', encoding='utf-8')
cadena  = ficher.read()
lista = []
l = []
l1 = []
#clase que busca dentro del documento html los tamaños de fuente para clasificarlos
#devuelve dos array que contienen los valores (tamaños y frecuencia) para analizar
#y segemetar el cv
#se esta considerando solamente el tamaño de la fuente para segementar

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag,attrs):
        if len(attrs) != 0:
            for i in attrs:
                if 'font-size' in i[1]:
                    lista.append(int(re.search('([0-9][0-9]*)',i[1]).group(0)))

parser = MyHTMLParser()
parser.feed(cadena)
ca = np.array(lista)
unique, count = np.unique(ca,return_counts =True)
l.append(unique)
l1.append(count)
print("Tamaño de fuentes en el documento :",l[0])
print("Frecuencia de los tamaños de fuentes:", l1[0])
print("la media de las fuentes es: ",int(np.mean(l)+1))


#buscar dentro de cada etiqueta con con una fuente mayor a la media y alamacenarlo en un array
class Busqueda(HTMLParser):

    def handle_starttag(self, tag, attrs):
        #..... 
        return attrs
        
    def handle_data(self, data):
        # .....
        return data
# pa =Busqueda()
# pa.feed(cadena)


#Grafica la distribucion del tamaño de fuente
# plt.bar(l[0], l1[0],color='orange',align='edge')
# plt.ylabel('Frecuencia de tamaño de fuente')
# plt.xlabel('Tamanode de fuentes')
# plt.title('Distribucion de tamaño de fuentes en un cv')
# plt.show()