# -*- coding: utf-8 -*-

'''
    Módulo encargado del análisis del texto

    Incluye las funcionalidades asociadas a Spacy y el diccionario con las stopwords utilizadas.
    
    -Stopwords: https://www.kaggle.com/rtatman/stopword-lists-for-19-languages#spanishST.txt
    -Spacy: https://spacy.io/
    -Versión más precisa pero menos eficiente de Spacy en español: https://github.com/pablodms/spacy-spanish-lemmatizer 


    Requisitos extra:
    -pip install spacy-langdetect
'''

import spacy
from spacy_langdetect import LanguageDetector


class Linguistic_Model():
    
    
    '''
        model_type: modelo de spacy utilizado. De forma predeterminada, utiliza el modelo 'es_core_news_sm'.
        stopwords_file: ubicación del fichero de stopwords que utilizará el sistema.
    '''
    def __init__(self, 
                 model_type='',
                 stopwords_file=''
                ):
        
        self._nlp=spacy.load(model_type)
        self._nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
        
        #Representado como diccionario para tener un tiempo de acceso menor.
        self._stopwords=self._load_stopwords(file=stopwords_file)

    '''
        MÉTODOS PRINCIPALES`
    ''' 
    
    '''
        Dado un texto, identifica el idioma.
        
        Input:
            -text: String. Texto del cual queremos obtener el idioma.
        
        Output:
            -String. Cadena de caracteres que identifica el lenguaje del texto.
    '''
    def detect_language(self,text=''):
        doc=self._nlp(text)
        return doc._.language['language'] 



    '''
        Lematiza un texto.
        
        Input:
            -sentence: String. Frase a lemanizar.
            
        Output:
            -String. Frase lemanizada.
    '''
    def lemmatize_using_spacy(self,sentence):
        result=''
        for token in self._nlp(sentence):
            result+=token.lemma_ + ' '

        return result
    
    '''
        Devuelve las stopwords utilizadas por el sistema.
        Los devuelve como diccionario para reducir el tiempo de búsqueda y acceso.
        
        Output:
            - Dict. Diccionario cuyas claves son las stopwords utilizas por el sistema. Los valores son None. 
    '''
    def get_stopwords(self):
        return self._stopwords

    '''
        MÉTODOS INTERNOS
    '''
    #Carga las stopwords del fichero donde están ubicados.
    def _load_stopwords(self, file=''):
        stopwords=dict()
        with open(file, 'r', encoding='latin-1') as file_pointer:
            content=file_pointer.read()
    
        for word in content.split():
            stopwords[word]=None
        
        return stopwords
        
        
