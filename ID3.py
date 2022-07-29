# Algoritmo id3 PARA COSNTRUIR UN ARBOL de descion

import numpy as np
import math
import uniout


def createDataSet():
    dataSet = np.array([['juventud', 'No', 'No', 'No'],
                    ['juventud', 'No', 'No', 'No'],
                    ['juventud', 'si', 'No', 'si'],
                    ['juventud', 'si', 'si', 'si'],
                    ['juventud', 'No', 'No', 'No'],
                    ['de edad mediana', 'No', 'No', 'No'],
                    ['de edad mediana', 'No', 'No', 'No'],
                    ['de edad mediana', 'si', 'si', 'si'],
                    ['de edad mediana', 'No', 'si', 'si'],
                    ['de edad mediana', 'No', 'si', 'si'],
                    ['mayor', 'No', 'si', 'si'],
                    ['mayor', 'No', 'si', 'si'],
                    ['mayor', 'si', 'No', 'si'],
                    ['mayor', 'si', 'No', 'si'],
                    ['mayor', 'No', 'No', 'No']])
    features = ['años', 'tener un trabajo', 'Propia casa']
    return dataSet, features


#calcularl la entropia de conjunto de datos
def calcEntropya(dataset):
    labels= list(dataset[:-1])
    prob= {}
    entropy =0.0
    for label in labels:
        prob[label]= (labels.count(label))/float(len(labels))
    for v in prob.values():
        entropy = entropy +(-v*math.log(v,2))

    return entropy



#conjunto de datos de petrtocion
def splitDataset(dataset, i, fc):
    subdataset = []
    for j in range(len(dataset)):
        if dataset[j,i]==str(fc):
            sbs = []

            sbs.append(dataset[j,:])
            subdataset.extend(sbs)

    subdataset = np.array(subdataset)
    return np.delete(subdataset,[i],1)



#calcule la ganancia de la informacion, seleccione la mejor caracteristica, para diidir elk coinjunto de datos, es decir que devuelva  el mejor indice de caracteristica
def chooseBestFeactureToSplit(dataset):
    labels = list(dataset[:,-1])
    bestInfGain = 0.0#ganancia maxima de informacion
    bestFeature = -1 #***********
    #Extraesr la conluma de caracteristicas y la collumna de etiquesta
    for i in range( dataset.shap[1]-1): #columnas
        #calcule la probabilidad de cada categoria
        prob ={}
        featureColumnsL = list(dataset[:,i])
        for fcl in featureColumnsL:
            prob[fcl]= featureColumnsL.count(fcl)/float(len(featureColumnsL))

            #calcule la entropia de cada categoria
            new_entropy = {}
            condi_entropy =0.0
            featureColumn = set(dataset[:,1])#columna de funciones
        for fc in featureColumn:
            subdataset = splitDataset(dataset, i,fc)
            prob_fc= len(subdataset)/float(len(dataset))
            new_entropy[fc]=calcEntropya(subdataset)#entropia de cada categoria
            condi_entropy = condi_entropy + prob[fc]*new_entropy[fc]#netropya condicional
            infoGain = calcEntropya(dataset)-condi_entropy#calcular de la ganancia de informacion
        if infoGain> bestInfGain:
            bestInfGain = infoGain
            bestFeature =i
    return bestFeature



#si la caracteristica del conjunto de caracteristicasestan vacias , emntonces t es una solo nodo
#la etiqueta de clase con el arbol de instancias mas granbde ene l conjunto de datos d se usa como la etiqueta
# de clase del noso y se devuelkve T

def mayorityLabelCount(labels):
    labelCount = {}
    for label in labels:
        if label not in labelCount.keys():
            labelCount[label] =0
        labelCount[label] +=1
    return max(labelCount)



#CONSTRUCCION DE ARBOL DE DESCCION
def createDecisionTree(dataset, features):
    labels= list(dataset[:,1])
##Si todas las instancias en el conjunto de datos pertenecen a la misma 
# ##etiqueta de clase, T es un árbol de un solo nodo, y la etiqueta de clase
 ##se usa como etiqueta de clase del nodo, y se devuelve T"""

    if len(set(labels)) ==1:
        return labels[0]
#si las caracteristicas del conjunto de carateristicas estan vacias,
#entonces T es un solo nodo, y las etiquestas de clñase con
# el arbol de inntancias mas grandes en el coinjunto de datis Dse usa
# como la etiqueta  de clase del nodo, y se devueklve T
    if len(dataset[0]) ==1:
        return mayorityLabelCount(labels)

        #de lo contrario , calvcules  la ganancia de informacion de cada caracteristicas
        # en el conjunto de cacracteristicas para el conmjkunto de  datos D de eacuerdo con 
        # el algoritmo ID3, y selecciona la caracteriticas con mayor ganancia de informacion , beatFuture
    bestFeatureI = chooseBestFeactureToSplit(dataset) #subindices de la mejor caracteristicas
    bestFeature = features[bestFeatureI]#Mejor caracteristicas
    decisionTree ={bestFeature:{}}#construccion un arboil cion la carateristica besFuture con la mayor ganancia
    # de informaicon coimo nodo hijo
    del(features[bestFeatureI])#esta funcion se ha utilizado comomun noido secundario, eliminala 
    #para que pueda continuar construyendo el subarbol
    bestFeatureColumn= set(dataset[:,bestFeatureI])
    for bfc in bestFeatureColumn:
        subFeatures = features[:]
        decisionTree[bestFeature][bfc] = createDecisionTree(splitDataset(dataset,bestFeatureI,bfc),subFeatures)
    return decisionTree


#categoria de datos de prueba
def classify(testData, features,decisionTree):
    for key in decisionTree:
        index = features.index(key)
        testData_value = testData[index]
        subTree = decisionTree[key][testData_value]
        if type(subTree)==dict:
            result = classify(testData,features,subTree)
            return result
        else:
            return subTree


if __name__ =="__main__":
    dataset,features = createDataSet()
    decisionTree = createDecisionTree(dataset,features)#construcicon del arbol de descion
    print('arbol de decision',decisionTree)
    dataset,features = createDataSet()
    testData = ['mayor','si','No']
    result = classify(testData, features,decisionTree)#Cataegrizar los datos de prueba
    print("ya sea para dar",testData,"prestamos",result)