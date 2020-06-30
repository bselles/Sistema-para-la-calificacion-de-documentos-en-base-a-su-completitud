# -*- coding: utf-8 -*-

'''
    Módulo de vectorización 
    
    Es el encargado de la comunicación con el modelo de Word2Vec pre-entrenado. 
    
    Este módulo permite convertir cadenas de caracteres en vectores ubicados en un espacio vectorial cuya ubicación representa su significado.
    
    Esta representación (una posición en el espacio vectorial) es la que se utilizará para comparar las distintas palabras que componene los textos.
    
'''


from gensim.models import KeyedVectors

class Words_Vectorization_Model():
    
    def __init__(self, 
                 pre_trained_model_file=''  #Ubicación del texto que almacena el modelo pre-entrenado de Word2vec.
                 ):
        
        self.model=self.__load_pre_trained_model(filename=pre_trained_model_file)
        
        
    '''
        MÉTODOS PRINCIPALES
    '''
    
    '''
        Dada una cadena de caracteres, devuelve su vector asociado.
            Input:
                -word: String. Término del cual queremos obtener el vector asociado.
                
            Output:
                -Vector de floats de 32: vector en el espacio vectorial definido por el modelo pre-entrenado que identifica unívocamente el término introducido. 
    '''
    def get_word_vector(self,word):
        return self.model[word]
    
    '''
        Dado un vector del espacio vectorial, devuelve su cadena de caracteres asociada.
            Input:
                -word_vector: Vector de floats de 32. vector del cual queremos obtener su término (string) asociado.
                
            Output:
                -String. Cadena de caracteres que representa el vector introducido.
    '''
    def get_original_word(self, word_vector):
        #Devolvemos el primer elemento
        return self.model.wv.most_similar(positive=[word_vector])[0][0]
        
    '''
        MÉTODOS AUXILIARES
    '''
    #Carga el modelo pre-entrenado de Word2Vec
    def __load_pre_trained_model(self,filename=''):
        return KeyedVectors.load_word2vec_format(filename, binary=False)
    
