# -*- coding: utf-8 -*-

'''
    Módulo encargado de la extracción de criterios y subcriterios asociados a los artículos.
'''

#Imports necesarios
import pandas as pd 
import re
import nltk
import spacy
import string
import numpy as np
from collections import OrderedDict
from spacy.lang.es.stop_words import STOP_WORDS
from multi_rake import Rake


'''
    Para utilizarlo, es necesario instalar el complemento de nltk de stopwords
    
    nltk.download('stopwords')
'''

        
'''
    Clase encargada de extraer potenciales criterios y subcriterios asociados a textos normativos.
    
    Permite analizar un texto en el que se descrube la norma que determina la evaluación de un tipo de documentos 
    para extraer distintos términos clave o relevantes que servirán como subcriterios por parte del sistema.
    
    Para ello, combina tres técnicas distintas:
        -TextRank: extrae 5 keywords de un único término.
        -Collocations extraction: Extrae 5 bigramas y 5 trigramas que tienden a co-ocurrir.
        -RAKE: aplicando Rapid Automatic Keyword Extraction, extrae una colección de n-gramas (max(n)=4) de interés.
        
'''


class Criteria_Extractor_Module():
    
    #Inicialización del sistema
    def __init__(self):
        self._model= spacy.load("") #modelo de spacy para el análisis del texto.
        self._tr=TextRank4Keyword(self._model) #Clase para el uso de TextRank    
        STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}
        self._spanish_stopwords=list(STOPWORDS_DICT['spanish']) #stopwords utilizadas

    '''
        Dado un documento en el que se define un criterio, lo analiza y extrae distinta información relevante para su identificación
        por parte del sistema. Esta información puede almacenarse en un nuevo fichero o concatenarse con la información de un
        fichero existente.
        
        Input:
            -criteria_name: String. Nombre del nuevo criterio.
            -articles_path: String. Ubicación del fichero del cual se desea extraer la información sobre los criterios.
            -write: Boolean. Flag que, en el caso de que sea true, los resultados se almacenarán en el fichero correspondiente. En el caso de que sea False, 
            tan solo se devolverá el resultado, sin escribirlo en ningún fichero
            -destination_file: String. Ubicación del nuevo fichero en el que se van a almacenar los resultados.
            -add: Boolean. Flag que indica que el resultado se va a almacenar en un fichero existente.
                -add== True: los resultados se añadirán a los criterios existentes en el fichero indicado en 'initial_file'.
                -add== False: los resultados se almacenarán en un nuevo fichero. Este será el indicado en 'destination_file'.
            -initial_file:  String. Ubicación del fichero en el que se van a concatenar los resultados en el caso de que add == True. 
    
    
        Output:
            -dict: diccionario con la información extraída del nuevo criterio.
    '''
    
    def criteria_extract(self,
                       criteria_name='',
                       articles_path='', 
                       ):

        with open(articles_path, "r", encoding='latin-1') as myfile:
            articulos= myfile.read()
            
        preprocessed=self._preprocess(articulos) #Procesado de la entrada
        coll_res=self._collocations_search(preprocessed)  #Resultado de la extracción mediante collocations
        tr_res= self._TextRank_search(preprocessed)  #Resultado de la extracción mediante TextRank
        rake_res=self._RAKE_search(articulos) #Resultado de la extracción mediante RAKE. Se hace sobre los textos originales (sin procesar).
        
        result=list(set(coll_res) | set(tr_res) | set(rake_res))   
        dict_result={criteria_name:[]}
        
        #Almacenamos los resultados
        for x in result:
            dict_result[criteria_name].append(x)
        
        return dict_result
        
        

    #Extracción de kw mediante RAKE
    def _RAKE_search(self,text, score_threshold=):
        rake=Rake(min_chars=, #Número mínimo de caracteres que debe tener un término para poder considerarse kw.
              max_words=, #Número máximo de términos que puede contener una potencial kw.
              min_freq=, #Frecuencia mínima de aparición.
              language_code='')
        keywords=rake.apply(text)
        
        result=list()
        for (x,y) in keywords:
            if y > score_threshold: #Puntuación mínima.
                result.append(x)
            
        return result
    
    #Extracción vía TextRank. Utiliza la clase descrita abajo.
    def _TextRank_search(self,text):
        self._tr.analyze(text, stopwords=self._spanish_stopwords)
        return self._tr.get_keywords(5)
    
    #Extracción analizando la co-ocurrencia de distintos términos del texto (collocations extraction)
    def _collocations_search(self,text):
        #Inicialización de los bigramas y trigramas.
        bigramFinder = nltk.collocations.BigramCollocationFinder.from_words(text.split())
        trigramFinder = nltk.collocations.TrigramCollocationFinder.from_words(text.split())
      
        #Obtenemos los 5 bigramas más frecuentes que aparecen en los artículos.
        bigramFreqTable = pd.DataFrame(list( bigramFinder.ngram_fd.items()),
                                       columns=['bigram','freq']).sort_values(by='freq'
                                               , ascending=False).head(5).reset_index(drop=True)
                
        #Obtenemos los 5 trigramas más frecuentes que aparecen en los artículos.
        trigramFreqTable = pd.DataFrame(list(trigramFinder.ngram_fd.items()),
                                        columns=['trigram','freq']).sort_values(by='freq',
                                                ascending=False).head(5).reset_index(drop=True)
        
        #Eliminamos la información innecesaria y formateamos su contenido.    
        parsed_bigrams=self._parse_tuple_to_string(bigramFreqTable['bigram'].values)
        parsed_trigrams=self._parse_tuple_to_string(trigramFreqTable['trigram'].values )
        
        return list(set(parsed_bigrams) | set(parsed_trigrams))   
    
    
    '''
        Aplica las transformaciones de los métodos que aparecen abajo sobre el texto.
        
        De esta forma, facilitamos al sistema la extracción de contenido relevante.
    '''
    def _preprocess(self,text):
        text=self._replace_punctuation(text, "") #Eliminamos los signos de puntuación
        text=self._remove_stopwords(text, self._spanish_stopwords) #Eliminamos las stopwords
        text= self._lemmanize_text(text) #lemanizamos el texto
        text= self._to_lowercase(text)
        return text
    
    '''
        Elimina los signos de puntuación del texto
    '''
    def _replace_punctuation (self,text, replace):
        return re.sub('[%s]' % re.escape(string.punctuation), replace, text)
        
    
    '''
        Elimina las palabras vacías/stopwords del texto
    '''
    def _remove_stopwords(self,text, stop_words):
        result=list()
        for x in text.split():
            if not x in stop_words:
                result.append(x)
                
        return " ".join(i for i in result)
     
    '''
        Dado un texto, lemaniza todas las palabras que contiene y lo devuelve.
    '''
    def _lemmanize_text(self,text):
        doc=self._model(text)
        lemma=[token.lemma_ for token in doc]
        return " ".join(i for i in lemma)    
    
    '''
        Convierte los caracteres de un texto entrante a minúsculas.
    '''
    def _to_lowercase(self,text):
        return text.lower()
    
    
    def _parse_tuple_to_string(self,criteria_tuple_list):
        result=list()
        for x in criteria_tuple_list:
            result.append(' '.join(list(x)))
        return result

'''
    Clase que aplica TextRank para extraer keywords de los artículos.
    
    Estas kw son de un único término. 
'''

class TextRank4Keyword():
   
    
    def __init__(self, model):
        self._d =  # Damping ratio. 
        self._min_diff = # Umbral de convergencia
        self._steps =  # Número de iteraciones
        self._node_weight = None # Almacenamiento de las kw y su peso

        self._model=model  #Modelo spacy para realizar el análisis del texto.

    '''
        Devuelve las 'number' kw más relevantes extraídas del texto.
    '''
    def get_keywords(self, number=10):
        node_weight = OrderedDict(sorted(self._node_weight.items(), key=lambda t: t[1], reverse=True))
        result=list()
        for i, (key, value) in enumerate(node_weight.items()):
            result.append(key)
            if i > number:
                return result
        
    '''
        Analiza el texto. Para cada término del texto le asocia un peso que determina su relevancia. 
    '''
    def analyze(self, text, 
                    candidate_pos=['NOUN', 'PROPN'], 
                    window_size=4, lower=False, stopwords=list()):        

            self._set_stopwords(stopwords)
            doc = self._model(text)
            sentences = self._sentence_segment(doc, candidate_pos, lower) 
            vocab = self._get_vocab(sentences)
            token_pairs = self._get_token_pairs(window_size, sentences)
            g = self._get_matrix(vocab, token_pairs)
            pr = np.array([1] * len(vocab))
    
            previous_pr = 0
            for epoch in range(self._steps):
                pr = (1-self._d) + self._d * np.dot(g, pr)
                if abs(previous_pr - sum(pr))  < self._min_diff:
                    break
                else:
                    previous_pr = sum(pr)
    
            # Para cada nodo, determinamos su peso.
            node_weight = dict()
            for word, index in vocab.items():
                node_weight[word] = pr[index]
                    
            self._node_weight = node_weight

    #Fija las stopwords que va a utilizar la instancia.  
    def _set_stopwords(self, stopwords):
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = self._model.vocab[word]
            lexeme.is_stop = True
    
    #Almacena las palabras que ocupan la posición candidata.
    def _sentence_segment(self, doc, candidate_pos, lower):
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    #Devuelve todos los tokens en forma de diccionario ordenado.
    def _get_vocab(self, sentences):
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    #Genera pares de tokens para procesarlos en el futuro.
    def _get_token_pairs(self, window_size, sentences):
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    #Devuelve la matriz simétrica.
    def _symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    #Devuelve la matriz normalizada.
    def _get_matrix(self, vocab, token_pairs):
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        g = self._symmetrize(g) #Obtiene la matriz simétrica.
        norm = np.sum(g, axis=0)  #La matriz se normaliza por la columna.
        
        return np.divide(g, norm, where=norm!=0) #Ignora 0

    