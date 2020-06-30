# -*- coding: utf-8 -*-


'''
    Módulo de análisis de texto
    
    Es el encargado del análisis y la comparación del contenido de uno o varios textos.
    
    Permite:
        -Comparar el contenido de dos sentencias.
        -Detectar el lenguaje asociado a un texto.
        -Procesar su contenido como corresponda.
'''

from linguistic_model import Linguistic_Model
from words_model import Words_Vectorization_Model
from numpy import dot
from numpy.linalg import norm
from sentence_processing import Text_Preprocessing_Module

class Text_Analyzer():
    
    def __init__(self, 
                 pre_trained_model_file='',
                 model_type='',
                 stopwords_file=''
                 ):
        
        self._linguistic_model=Linguistic_Model(model_type=model_type, stopwords_file=stopwords_file) #Módulo encargado de análisis del texto.
        self._words_vectorization_model= Words_Vectorization_Model(pre_trained_model_file= pre_trained_model_file) #Módulo de vectorización 
        self._text_pre_processing_module= Text_Preprocessing_Module(linguistic_model=self._linguistic_model) #Módulo de pre-procesamiento de textos.
        
    '''
        MÉTODOS PRINCIPALES
    '''

    '''
        Determina si un concepto aparece en una cierta sentencia. El resultado es un valor real entre 0 y 1 (no aparece ni parcialmente y aparece totalmente, respectivamente).
        
        Tanto el concepto como la sentencia se representan mediante dos parámetros: X_vect y X_others.
        
        X_vect almacena los términos de la sentencia o del concepto que tienen representación dentro del espacio vectorial generado por el modelo de Word2vec utilizado. Dicho
        de otra forma, son aquellos términos que el sistema ha conseguido generar una representación válida y relevante en forma de vector.
        
        X_others almacena los términos de la sentencia o del concepto que no tienen una representación entro del espacio vectorial. En este caso, se representan mediante cadenas de caracteres.
        Suelen consistir en acrónimos, anglicismos, fragmentos del texto mal redactados, etc.
        
        Input:
            - concept_vect: vector con los vectores que representan los términos del concepto.
            - concept_others: vector con los términos que no pueden representarse como vectores que contiene el concepto. Estos se representan mediante cadenas de caracteres.
            - sent_vect: vector con los vectores que representan lso términos de la sentencia.
            - sent_others: vector con los términos que no pueden representarse como vectores que contiene la sentencia. Estos se representan mediante cadenas de caracteres.
        
        Output:
            - Valor real entre 0 y 1 que determina el grado en el que el concepto aparece en la sentencia. 0 implica que no aparece en absoluto. 1 implica que aparece totalmente.
    '''
    def compare_sentences(self,
                          concept_vect,
                          concept_others,
                          sent_vect,
                          sent_others
                          ):
        
        return self._compare_sentences_average_mode(concept_vect, concept_others, sent_vect, sent_others)
            
            
    '''
        Preprocesa, tal y como se describe en el módulo de preprocesamiento de textos del sistema, la sentencia introducida.
        
        Input: 
            -sentence: String. Cadena de caracteres que representa la sentencia a procesar.
        
        Output:
            -String. Cadena de caracteres que representa la sentencia procesada. 
            -Boolean. En el caso de que el resultado sea irrelevante (sea una sentencia vacía, un espacio en blanco, etc), este método devolverá False.
    '''
    def preprocess(self,sentence):
        return self._text_pre_processing_module.process_sentence(sentence)
    
    '''
        Dada una sentencia, le aplica el preprocesamiento descrito en el módulo de preprocesamiento de sentencias del sistema y luego obtiene los vectores asociados a cada término de la misma.
        
        Input:
            -sentence: String. 
            
        Output:
            -Lista. Lista cuyos elementos son los términos de la sentencia representados como vectores. Incluye tan solo los que pueden representarse como vectores.
            -Lista. Lista cuyos elementos son los términos de la sentencia que no pueden representarse como vectores. Estos, se representan mediante las cadenas de caracteres (strings) originales.
            -Bool. En el caso de que la sentencia introducida no sea relevante (esté compuesta tan solo por espacios en blanco, símbolos extraños, etc), devuelve False.
        
    '''
    def transform(self,sentence):
        #Parte 1: procesamos la frase correspondiente. Si devuelve False, implica que el contenido es irrelevante.
        processed_sentence= self._text_pre_processing_module.process_sentence(sentence)
        
        #Si la frase resultante no es relevante (es un espacio en blanco, etc)
        if not processed_sentence:
            return False, False
        
        #Parte 2: Vectorizamos la frase
        return self._vectorize_sentence(processed_sentence)
    
    '''
        Dado un texto, devuelve el lenguaje en el que está escrito.
        
        Input:
            -text. String.
            
        Output:
            -String. cadena de caracteres que representa el lenguaje en el que está escrito el texto.
    '''
    def detect_language(self, text):
        return self._linguistic_model.detect_language(text=text)
    
    
    '''
        MÉTODOS INTERNOS
    '''
    
    
    '''
        Dada una sentencia, devuelve dos listas:
            1. Lista de vectores float32. La lista contiene un vector por cada palabra de la frase 
            que forma parte del vocabulario del modelo pre-entrenado que utiliza el sistema.
    
            2. Lista de strings. La lista contiene un string por cada palabra de la sentencia que no 
            forma parte del vocabulario del modelo pre-entrenado que utiliza el sistema. Suelen consistir 
            en acrónimos, anglicismos, etc.
    '''     
    def _vectorize_sentence(self,sentence):
        vector, others= [],[]
        for word in sentence.split():
            try:
                vector.append(self._words_vectorization_model.get_word_vector(word))
            except:
                others.append(word)
            
        return vector, others
    
    #Dados dos vectores que representan dos términos, calcula su semejanza en base a la semejanza de cosenos.
    def _get_cosine_similarity(self,word1, word2):   
        return dot(word1,word2)/(norm(word1)*norm(word2))
    
    '''
        Compara dos términos atendiendo al longest common substring entre ellos.
        
        El resultado consiste en el porcentaje (entre 0 y 1) de caracteres comunes, atendiendo 
        a la media de los caracteres de ambos términos.
    '''
    def _compare_longest_common_substring(self,X,Y):
        m, n=len(X), len(Y)
        
        #Sufijos
        LCSuff = [[0 for k in range(n+1)] for l in range(m+1)] 
        
        result = 0 
        for i in range(m + 1): 
            for j in range(n + 1): 
                if (i == 0 or j == 0): 
                    LCSuff[i][j] = 0
                elif (X[i-1] == Y[j-1]): 
                    LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                    result = max(result, LCSuff[i][j]) 
                else: 
                    LCSuff[i][j] = 0
                    
        #result almacena el longest common substring.
        return result/((m+n)/2)
      
    #Devuelve la semejanza existente entre dos sentencias. Esta semejanza se calcula a partir de la media de la semejanza 
    #máxima existente entre los términos del concepto y los términos de la sentencia en la que se busca dicho concepto.
    def _compare_sentences_average_mode(self,concept_vect, concept_others, sent_vect, sent_others):
        #Si el concepto tiene términos que no pertenecen al vocabulario del modelo entrenado.
    
        num_terms=0
        if len(concept_others)!=0:    
            for x in concept_others:
                max_value=0
                for y in sent_others:
                    curr= self._compare_longest_common_substring(x,y)
                    if curr > max_value:
                        max_value=curr
                
                num_terms+=max_value
        
        average_vects=0
        for x in concept_vect:
            best=0
            for y in sent_vect:
                curr=self._get_cosine_similarity(x,y)
                if curr> best:
                    best=curr
                    
            average_vects+=best
        
        return (num_terms + average_vects)/(len(concept_vect)+len(concept_others))            