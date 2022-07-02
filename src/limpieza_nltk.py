import nltk
from nltk.corpus  import stopwords
from tqdm import tqdm
import time as ti

nltk.download('stopwords')
#cambiar los caracteres que se tien utf8 por letras  normales 
def normalize(s):
    replacements =(
        ("á","a"),
        ("é","e"),
        ("í","i"),
        ("ó","o"),
        ("ú","u"),
    )
    for a,b in replacements:
        s = s.replace(a,b).replace(a.upper() ,b.upper())
    return s

with open('texto.text',encoding ='ISO-8859-1',errors='ignore') as f:
    content =f.read()
    tokenize =nltk.word_tokenize(content)
    #realizamos la limpieza del texto 
    token_limpio = []
    #guardar stopword español paa limpiar texto
    guardar =True
    for i in tqdm(tokenize):#sirve para crear una barra de progreso
        for word in stopwords.words('english'):
            if (word.lower() == i.lower() ):
                #si existen no lo guarda
                guardar = False
        if(guardar):
            if(len(i)>2):
                    #guardar las palabras que no estan en stopwords y saca  caracteres como .. entre otros
                token_limpio.append(normalize(i))
        guardar = True

#A partir de aqui se realiza el emparejamiento segun el tipo de palabra que se leyo
tag = nltk.pos_tag(token_limpio)
print(tag)
#print(token_limpio)