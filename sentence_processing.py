# -*- coding: utf-8 -*-

'''
    Módulo de procesamiento de sentencias
    
    Dada una sentencia, aplica las siguientes transformaciones:
        1- Transforma los caracteres del texto a minúsculas.
        2- Elimina los términos numéricos.
        3- Elimina los signos extraños. Estos son los símbolos que no son alfabéticos.
        4. Lematiza el contenido.
        5- Elimina los espacios en blanco redundantes.
        6- Elimina las stopwords.
        7- Elimina los términos con un único caracter.
'''
import re

class Text_Preprocessing_Module():
    
    def __init__(self, 
                 linguistic_model=''):
        
        self.linguistic_model=linguistic_model    
        
    '''
        MÉTODO PRINCIPAL
    '''
    
    '''
        Procesa la sentencia introducida aplicando las transformaciones descritas arriba.
        
        Input:
            -sentence: String. Cadena de caracteres que representa la sentencia a procesar.
            
        Output:
            -String. Cadena de caracteres que representa la sentencia introducida con las transformaciones realizadas (procesada).
            -Bool. En el caso de que, después de realizar las transformaciones, su contenido sea irrelevante (sea solo espacios en blanco, la sentencia tan solo contenga símbolos extraños, etc),
            el método devolverá el booleano False.
    '''
    def process_sentence(self,sentence):
        if sentence.isspace() or sentence=='':
            return False
        
        sentence=self.__lower_text(sentence)
        sentence=self.__erase_numeric_words(sentence)
        sentence=self.__erase_strange_signs(sentence)
        sentence=self.__lemmatize(sentence)
        sentence=self.__erase_useless_whitespaces(sentence)
        sentence=self.__remove_stopwords(sentence)
        sentence=self.__remove_single_character_words(sentence)
        
        if sentence.isspace() or sentence=='':
            return False
        
        return sentence
    
    '''
        MÉTODOS AUXILIARES
    '''
    #Elimina los términos numéricos
    def __erase_numeric_words(self,text):
        return re.sub(r'\w*\d\w*', '', text)
    
    #Elimina los signos que no son alfabéticos de un texto. En el caso de que formen parte de una palabra (p.e: "Información), elimina solo el signo (quedaría solo Información)
    def __erase_strange_signs(self,text):
        result=''
        for x in text.split():            
            
            if len(x)>1:
                if x.isalpha():
                    result+= x + ' '
                else:
                    result+= self.__erase_non_alphabetical_characters(x) + ' '
            else:
                if x.isalpha():
                    result+= x + ' '
    
        return result
    
    #Elimina los espacios en blanco redundantes o innecesarios.
    def __erase_useless_whitespaces(self,text):
        return " ".join(text.split())
    
    #Elimina los caracteres no alfabéticos de un término.
    def __erase_non_alphabetical_characters(self,word):
        result=''
        for char in word:
            if char.isalpha():
                result+=char
        return result
    
    #Lematiza el contenido de un texto.
    def __lemmatize(self,text):
        return self.linguistic_model.lemmatize_using_spacy(text)
    
    #Elimina las palabras formadas por un único término.
    def __remove_single_character_words(self,text):
        result=''
        for word in text.split():
            if len(word)>=2:
                result+= word + ' '
        
        return result
        
    #Elimina las stopwords del texto.
    def __remove_stopwords(self,text):
        result=''
        for word in text.split():
            if not word in self.linguistic_model.get_stopwords().keys():
                result+= word + ' '
                
        return result
            
    #Devuelve el texto con los caracteres convertidos a minúscula.
    def __lower_text(self,text):
        return text.lower()


