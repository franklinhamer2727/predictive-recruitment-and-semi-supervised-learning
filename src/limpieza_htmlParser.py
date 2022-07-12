from html.parser import HTMLParser
from calendar import c
import re
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests



ruta = 'html_limpio/20.html'
ficher = open(ruta,'r', encoding='utf-8')
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



#funcion que realiza un conteo de las frecuecia de repeticion de tamaño de fuente 
def conteo_size(lista):
    ca = np.array(lista)
    unique, count = np.unique(ca,return_counts =True)
    l.append(unique)
    l1.append(count)
    
    print("Tamaño de fuentes en el documento :",l[0])
    print("Frecuencia de los tamaños de fuentes:", l1[0])
    print("la media de las fuentes es: ",int(np.mean(l)+1))
    return  l

l = conteo_size(lista)
print(l1[0])
frec = []
size = []
#funcion que elimina  no claifica las palabras que no se repiten mas de dos veces con el fin de tener valores mas exactos 
# al momento de encontrar etiquetas de como los son skill, profile, project, etc
def arreglos(l,l1):
    size =l[0]
    frec = l1[0]
    i =0 
    while i <len(frec):
        if frec[i]<=3:
            frec = np.delete(frec,i)
            size = np.delete(size,i)
            print("se elimino la posicion ",i)
            print("h",frec)
            print("tamaños",size)
            i = 0
        else:
            i =1+i
    return np.max(size),frec,size

valor,array_frec,array_size =arreglos(l,l1)

valor = valor
#buscar dentro de cada etiqueta con con una fuente mayor a la media y alamacenarlo en un array
class header_bloques(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data= []
        self.capture =False
    def handle_starttag(self,tag,attrs):
        if tag in ('span'):
            if len(attrs)!=0:
                for i in attrs:
                    if 'font-size:'+str(valor)+'px' in i[1]:
                        self.capture=True
    def handle_endtag(self, tag):
        if tag in ('span'):
            self.capture=False
    def handle_data(self, data):
        if self.capture:
            self.data.append(data)

parserr = header_bloques()
parserr.feed(cadena)

#print(parserr.data)

print(array_size)


class body_bloques(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data= []
        self.capture =False
        self.cont =0
    def handle_starttag(self,tag,attrs):
        if tag in ('span'):
            if len(attrs)!=0:
                for i in attrs:
                    #print("hola",self.cont)
                    if 'font-size:'+str(valor)+'px'  in i[1]:
                        self.cont= self.cont+1
                    if self.cont ==1:
                        
                        self.capture=True
                    # if self.cont >1:
                    #     print("que tal")
                    #     self.cont= 1

    def handle_endtag(self, tag):
        if tag in ('span'):
            self.capture=False
    def handle_data(self, data):
        if self.capture:
            self.data.append(data) 

parsr = body_bloques()
parsr.feed(cadena)
f = parsr.data
print(f)
import os

d= open("datos.txt","w")
d.write(str(f))
d.close()

#Grafica la distribucion del tamaño de fuente
# plt.bar(l[0], l1[0],color='orange',align='edge')
# plt.ylabel('Frecuencia de tamaño de fuente')
# plt.xlabel('Tamanode de fuentes')
# plt.title('Distribucion de tamaño de fuentes en un cv')
# plt.show()