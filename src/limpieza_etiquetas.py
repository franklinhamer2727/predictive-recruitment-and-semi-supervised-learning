from calendar import c
import re
ficher = open('html\\25.html','r', encoding='utf-8')
cadena  = ficher.read()
#Para eliminar los  los spam vacios
def limpiarTexto(nuevoTexto):
    
    nuevoTexto = re.sub('(<(span*\w+)\s[^>][^>]*><\/span*\w+>)', '',nuevoTexto)# para eliminar las lineas innecesarias
    nuevoTexto = re.sub('(<br>)', '', nuevoTexto)#para eliminar los espacios innecesarios
    
    nuevoTexto = re.sub('<span style=(\".*?font\-size):','<span style="font-size:',nuevoTexto) #eliminar atributos de la etiqueta style y solo dejar el tamañano de letra
    nuevoTexto= re.sub('<div\W* style=(\".*?\")>','<div>',nuevoTexto) #Eliminar las etiquetas del div
    nuevoTexto = re.sub('(<(span*\w+)\s[^>][^>]*>\W+<\/span*\w+>)','',nuevoTexto) #eliminar los caracteres extraños 
    return nuevoTexto
b = limpiarTexto(cadena)
#print(b)
Html_file= open("html_limpio\\25.html","w",encoding='utf-8')
Html_file.write(b)
Html_file.close