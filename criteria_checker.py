# -*- coding: utf-8 -*-

'''
    Módulo encargado de analizar el cumplimiento de un cierto criterio dentro de un documento.
    
    Para ello, analiza la aparición de los distintos subcriterios que lo componen dentro del propio documento.
'''


from text_analyzer import Text_Analyzer
from utilities import configuration 

class Criteria_Checker():
        
    def __init__(self,
                 pre_trained_model_file='',
                 model_type='',
                 stopwords_file=''
                 ):
        

        
        self.text_analyzer=Text_Analyzer( pre_trained_model_file=pre_trained_model_file,
                                             model_type=model_type,
                                             stopwords_file=stopwords_file)

        print('Text analyzer loaded.')
             
    '''
        MÉTODOS PRINCIPALES
    '''
    
    '''
        Dado un texto ya procesado, determina si un criterio se cumple. Para ello, evalúa la aparición de los subcriterios asociados al criterio.
        
        Input:
            -criterion_pos: Int. Posición dentro de la totalidad de los criterios evaluados que ocupa el criterio actual.
            -subcriteria: List. Lista que almacena los subcriterios asociados al criterio evaluado.
            -processed_text: String. Cadena de caracteres que representa el texto (ya procesado) en el cual queremos evaluar si se cumple el criterio.
            -autoconfigure_flag: Boolean. Determina si la ejecución forma parte del aprendizaje del sistema.
            -get_found: Boolean. Determina si la ejecución forma parte del análisis de los criterios utilizados por el sistema.
            
        Output:
            Si get_found == True:
                - Boolean. Indica si se cumple el criterio. True implica que se cumple. False, implica lo contrario.
                - Float. Indica el porcentaje de subcriterios encontrados. Es un valor entre 0 y 1 (no se ha encontrado ningún subcriterio y se han encontrado todos los subcriterios, respectivamente).
                - List. Lista con los subcrierios encontrados. Cada subcriterio se representa mediante su String correspondiente.
                
            Si no:
                - Boolean. Indica si se cumple el criterio. True implica que se cumple. False, implica lo contrario.
                - Float. Indica el porcentaje de subcriterios encontrados. Es un valor entre 0 y 1 (no se ha encontrado ningún subcriterio y se han encontrado todos los subcriterios, respectivamente).
    '''

    def check_criterion(self,
                        criterion_pos,
                        subcriteria,
                        processed_text,
                        autoconfigure_flag=False,
                        get_found=False
                        ):
        
        found_num=0
        found_concepts=[] #Lista con los criterios encontrados.
        
        rest=len(subcriteria)
            
        for subcriterion in subcriteria:
            found, value= self._check_concept(subcriterion, processed_text)
            rest-=1
            if found:
                found_num+=1
                found_concepts.append(subcriterion)
                            
                if (not autoconfigure_flag) and self._got_result(criterion_pos, found_num, len(subcriteria), rest):
                    if get_found:
                        return found_num/len(subcriteria)>= self._get_curr_threshold_value(criterion_pos),(found_num/len(subcriteria)), found_concepts 
                    else:
                        return found_num/len(subcriteria)>= self._get_curr_threshold_value(criterion_pos),(found_num/len(subcriteria)) 
        
        if get_found:
            return found_num/len(subcriteria)>= self._get_curr_threshold_value(criterion_pos),(found_num/len(subcriteria)), found_concepts 
        else:
            return found_num/len(subcriteria)>= self._get_curr_threshold_value(criterion_pos),(found_num/len(subcriteria)) 
        
        
    '''
        Atendiendo a las funcionalidades del módulo de análisis de textos del sistema, preprocesa el contenido de un documento completo. 
        
        Dado un texto, lo separa por sentencias y, sobre cada sentencia, aplica las transformaciones descritas en el módulo de análisis de textos.
        Estas transformaciones también implican la conversióna vectores de los términos (si es posible).
        
        Input:
            -text: String. Texto a procesar.
            
        Output:
            -List. Lista cuyos elementos son las sentencias del texto procesado. Cada sentencia consiste en una tupla de dos elementos:
                -Una lista con las representaciones como vectores de los términos que aparecen en el espacio vectorial definido por el modelo de Word2vec utilizado.
                -Una lista con los términos (string) que no aparecen en el espacio vectorial. 
        
    '''
        
    def pre_process_text(self, text):
        result=list()
        for paragraph in text.split('\n'):
            for sentence in paragraph.split('.'):
                sent_vect, sent_others=self.text_analyzer.transform(sentence)
                
                #Si sent_vect == False, el contenido de la línea es irrelevante (es un espacio en blanco, retorno de carro, etc)
                if sent_vect!=False:
                    result.append((sent_vect, sent_others))
                    
        return result
    
    '''
        MÉTODOS AUXILIARES
    '''
    #Busca un concepto (subcriterio) dentro de un texto.
    def _check_concept(self,
                        concept,
                        processed_text
                        ):
        
        concept_vect, concept_others = self.text_analyzer.transform(concept)
        
        if concept_vect == False:
            return False, False
        
        best=0
        for line in processed_text:        
            sent_vect=line[0]    
            sent_others=line[1]
            
            #Utilizamos el método average. Lo indicamos por parámetro de configuración.
            curr= self.text_analyzer.compare_sentences(concept_vect, concept_others, sent_vect, sent_others)
    
            if curr > best:
                best=curr
    
                if curr>= configuration['threshold_value']:
                    return True, curr
        
        return False, best
    
    
    #Determina si ya hemos alcanzado un resultado (si no es necesario seguir).
    def _got_result(self,
                    criterion_pos,
                    num_found, 
                    num_total, 
                    rest
                    ):
        
        curr_threshold= self._get_curr_threshold_value(criterion_pos)
        return (num_found/num_total)>= curr_threshold or (num_found+rest)/num_total < curr_threshold
        
        
    #Devuelve el kw_threshold_value asociado al criterio actual
    def _get_curr_threshold_value(self,
                                  criterion_pos
                                  ):
            
        return configuration['kw_threshold_value'][criterion_pos] if (criterion_pos in configuration['kw_threshold_value'].keys()) else configuration['default_threshold']
    

            
   