# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import warnings
import time
import os
import re
import urllib.request as urllib2
import time
import string

warnings.filterwarnings('ignore')
sns.set()

"""_____"""


def remove_bad_lines(text_lines):
    '''
    Función que quitará (borrará) las líneas de texto que no son utiles o necesarias para el lenguajes que se analiza.

    Parámetros
    ----------
    text_lines: (String) Líneas de texto

    Retorno
    -------
    text_lines:
    '''
    # Linea por linea
    bad_lines = []
    for line in text_lines:
        if(len(line.replace(' ', '')) <= 2): bad_lines.append(line)  # si la longitud de la linea es menos de 1
        #elif(not bool(re.search('[a-z]', line))): bad_lines.append(line)  # si no contiene minusculas
        elif('indd' in line): bad_lines.append(line)  # si hace referncia al indice de una pagina
        elif(('a.m.' in line) or ('p.m.' in line) or ('AM' in line) or ('PM' in line)): bad_lines.append(line)
        elif(('www' in line) or ('Ministerio' in line) or ('Lima' in line) or ('Perú' in line)): bad_lines.append(line)
        elif('-' in line):  # Para casos tipo [ko - no - ya ko-no-ya]
            aux = line.replace(' - ', '-')
            n_tokens = len(aux.split(' '))
            n_sub = len(aux.split('-'))
            if(n_sub > n_tokens): bad_lines.append(line)
    for bd in bad_lines:
        text_lines.remove(bd)
    return text_lines


def clean_sentences(sentences):
    '''
    Función que realizará la limpieza de las oraciones retirando caracteres no alfanuméricos ni signos de puntuación
    conocidos.

    Parámetros
    ----------
    sentences:  (String) oraciones con posibles caracteres no deseados (símbolos).

    Retorno
    -------
    clean_sentences: (String) oraciones limpias (sin símbolos extraños).
    '''
    puntuation = '!"#$*,-/<=>?[\]:^_`{|}~—¿•¡“”…»«º²ª¼¾°½√φε✓'
    print("las puntuaciones son: ",puntuation)
    clean_sentences = []
    for sent in sentences:
        # quitar numeros \d+ quitaba numeros
        clean_sent = re.sub(r'', '', sent)
        # quitar puntucacion
        clean_sent = ''.join(ch for ch in clean_sent if ch not in puntuation)
        # quitar multiples espacios en blanco
        while(clean_sent.find('  ')!=-1): clean_sent = clean_sent.replace('  ', ' ')
        # oraciones con palabras repetidas
        tokens = clean_sent.split(' ')
        vocab = list(set(tokens))
        if(len(vocab)/len(tokens) <= 0.25): continue
        clean_sentences.append(clean_sent)
    return clean_sentences


def obtain_sentences(text_file, out_file):
    '''
    Función que realizará la obtención de oraciones limpias (sin símbolos extraños ni texto no deseado).

    Parámetros
    ----------
    text_file:  (File) archivo de donde se extraerán las oraciones para su procesamiento.
    out_file:   (File) archivo donde se almacenarán las oraciones limpias.

    Retorno
    -------
    info: (DataSet) Retorna un DataSet con información sobre la cantidad total de líneas, cantidad de líneas limpias y
    cantidad de oraciones limpias.
    '''
    info = {}
    file = open(text_file, "r", encoding="utf-8")
    text = file.read()
    # quitar lineas inservibles
    text_lines = text.split('\n')
    info['n_lines'] = len(text_lines)  # lineas totales
    text_lines = remove_bad_lines(text_lines)
    info['n_clean_lines'] = len(text_lines)  # lineas limpias
    clean_text = '\n'.join(text_lines).replace('\’', '\'')  
    # limpiar caracteres
    clean_text = clean_text.replace('\n', ' ').replace('\t', ' ').replace('\x0c', ' ').replace('’', '\'').replace('‘', '\'').replace('´', '\'')
    clean_text = clean_text.replace('\uf097', ' ').replace('\uf043', ' ').replace('\u0094', ' ').replace('\x94', ' ').replace('\uf022', ' ')
    clean_text = clean_text.replace('ﬂ ', 'fl').replace('ﬁ ', 'fi')
    # oraciones
    sent_regex = re.compile("[A-Z].*?[a-z]+[\.|\:|\?]")  # regex para obtener oraciones
    sentences = re.findall(sent_regex, clean_text)
    clean_sents = clean_sentences(sentences)
    info['n_sentences'] = len(clean_sents)
    # guardar archivos de oraciones
    out_file = open(out_file, "w+", encoding="utf-8")
    out_file.write('\n'.join(clean_sents))
    alph = ''.join(set(''.join(clean_sents)))
    #print(alph)
    return info


"""___"""


def process_files(files_names,finfo_name):
    '''
    Función principal que inicia el procesamiento de los archivos para su limpieza (eliminación de símbolos y textos que
     no pertecen al lenguaje que se suministra).

    Parámetros
    ----------
    files_names:    (File) nombre del archivo que se va procesar.
    target_lang:    (String) Nombre del lenguaje que se está trabajando.
    finfo_name:     (File)  Nombre del archivo donde se almacenarán los datos obtenidos de las oraciones procesadas.

    Retorno
    -------
    Aparecerán archivos de texto plano con las oraciones limpias y un archivo CSV con información de lo procesado.
    '''
    docs_info = []
    for source_file in files_names:
        # Obtener los archivos de texto
        text_file = os.path.join(r'C:\Users\Hammer\Desktop\venv\venv\src\pdf',  source_file)
        # print(text_file)
        out_file = os.path.join(r'C:\Users\Hammer\Desktop\venv\venv\src\newtxt', source_file)
        # print(out_file)
        # print(source_file)
        # Obtener el texto limpio
        info = obtain_sentences(text_file, out_file)
        info['file'] = source_file
        # print(info)
        docs_info.append(info)
    df = pd.DataFrame(docs_info)
    df.to_csv(finfo_name, index=False)



file_names = os.listdir(r"C:\Users\Hammer\Desktop\venv\venv\src\pdf")
csv_data =pd.DataFrame(file_names)
finfo_name = r"C:\Users\Hammer\Desktop\venv\venv\src\data.csv"
# print(csv_data)
process_files(file_names,finfo_name)

