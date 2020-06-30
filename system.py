# -*- coding: utf-8 -*-

'''
    Controlador del sistema.

    Es el punto de acceso a las distintas funcionalidades que ofrece el sistema propuesto. Es el encargado
    de interacturar con los demás componentes del sistema para utilizar sus capacidades y para, conjuntamente, realizar
    su labor como sistema: evaluar documentos en base a su completitud a partir de unos criterios definidos.
    
'''

from learning_module import Learning_Module
from remodeling_module import Remodeling_Module
from criteria_checker import Criteria_Checker
from criteria_extractor_module import Criteria_Extractor_Module 
from utilities import read_criteria, configuration 
import json
import os

class System():    
    def __init__(self,
               pre_trained_model_file='',
               model_type='',
               stopwords_file='',
               criteria_file='',
               configuration_file='',
               kw_threshold_value={},
               min_text_size=
               ):

        configuration['configuration_file']=configuration_file
        configuration['kw_threshold_value']=kw_threshold_value
        configuration['min_text_size']=min_text_size
        
        self._criteria= read_criteria(criteria_file) if criteria_file!='' else ''
        
        
        #Inicialización de los demás componentes del sistema.
        self._cc=Criteria_Checker(pre_trained_model_file=pre_trained_model_file,
                                 model_type=model_type,
                                 stopwords_file=stopwords_file)
        
        self._rm= Remodeling_Module(text_analyzer=self._cc.text_analyzer)
        
        self._lm= Learning_Module()
        self._cem= Criteria_Extractor_Module()


    '''
        MÉTODOS PRINCIPALES
    '''
    
    
    '''
        Extrae información de un fichero para constituir un nuevo criterio. Extrae información asociada a un criterio, 
        el cual se almacenará en el sistema.
        
        Input:
            -criteria_name: String. Nombre del nuevo criterio que se va a crear.
            -articles_path: String. Ubicación/nombre del fichero del cual se desea extraer la información asociada a
            un criterio.
            
        Output:
            -Ninguna.
            
            Esta función realiza modificaciones dentro del sistema, no devuelve nada. Después de utilizar esta funcionalidad,
            el sistema tendrá un criterio más a través del cual puede realizar evaluaciones.
            
            Este nuevo criterio se añadirá a los que previamente se almacenan en el sistema (en la última posición).
    
    '''
    def criteria_extraction(self,
                            criteria_name='',
                            articles_path='', 
                       ):
        
        print('La información extraída se almacenará en el sistema. El nombre del criterio asociado es ', criteria_name)
        

        new_crit=self._cem.criteria_extract(criteria_name=criteria_name,
                                   articles_path=articles_path
                                   )
    
        #Almacenamos la nueva información extraída.    
        if self._criteria == '':
            self._criteria = dict()

        self._criteria.update(new_crit)
               
    '''
        Reestablece la configuración del sistema a su versión predeterminada.
        
        Esto implica eliminar la información asociada a los criterios utilizados 
        para realizar evaluaciones y sus umbrales.
        
        Input:
            -min_text_size: Entero. Número de términos mínimo que debe tener un documento
            para considerarse válido.
            
        Output:
            -Ninguna. Esta operación modifica el sistema internamente (estableciendo la configuración
            predeterminada) de modo que no devuelve nada.
    '''
    def restart_system_configuration(self, min_text_size=,
                                     configuration_file=''):
        configuration['configuration_file']=configuration_file
        
        configuration['threshold_value']=
        configuration['kw_threshold_value']={}
        configuration['default_threshold']=
        configuration['min_text_size']=min_text_size
        
        self._criteria=''
    
    
    '''
        Modifica los criterios que se utilizan para realizar las evaluaciones.
        
        Elimina los crierios preexistentes e introduce los presentes en un fichero (.txt).
        
        Input:
            -criteria_file: String. Ubicación/nombre del fichero (.txt) que contiene los criterios (y subcriterios)
            que se desean utilizar para realizar las evaluaciones.
            
        Output:
            -Ninguno.
    '''
    def set_criteria(self, criteria_file):
        self._criteria=read_criteria(criteria_file)
        
        print('Establecidos los criterios presentes en el documento ', criteria_file)
    
    
    
    '''
        Evalúa la calidad de un documento en base a una serie de criterios.
        
        Input:
            -criteria: diccionario Python. Incluye, como claves, la representación de los criterios que se desean evaluar
                y como valores los subcriterios asociados a cada criterio.
            
                Por ejemplo: {'Habla de RGPD': ['RGPD', 'Reglamento General de Protección de Datos']}
                
                En el caso de que no se indique por parámetro los criterios que se quieren utilizar, el sistema utilizará los criterios
                y subcriterios almacenados en el sistema. Si el sistema no tiene ninguno almacenado, muestra un mensaje de error.
               
                
        Los demás parámetros consisten en parámetros de funcionamiento interno del sistema, de modo que para el uso
        de un usuario, no son relevantes.
        
        Output:
            -Lista Python. Lista con un elemento por cada criterio evaluado. Estos elementos consistirán en cadenas de caracteres
            que representarán si se cumple dicho criterio (OK) o no se cumple (KO).
            
        
    '''
    def check_document(self,
                       criteria=dict(),
                       text='',
                       autoconfigure_flag=False,    #Flags de funcionamiento interno. Ignorar.
                       get_found=False
                       ):
                
        #Vemos si utilizamos los criterios del sistema o unos externos.
        criteria=self._init_criteria(criteria)
        
        if criteria=='':
            return 'No se han especificado los criterios para realizar la evaluación.'
    
        if self._rm.check_text_validity(text):     
            
            return self._check_criteria(criteria=criteria,
                                        text=text,
                                        autoconfigure_flag=False,
                                        get_found=False,
                                        clean=True)        
        else:
            return "El documento introducido no es válido."
  
    
    '''
        Evalúa la calidad de una colección de documentos en base a una serie de criterios.
        
        Input:
            -criteria: diccionario Python. Incluye, como claves, la representación de los criterios que se desean evaluar
                y como valores los subcriterios asociados a cada criterio.
            
                Por ejemplo: {'Habla de RGPD': ['RGPD', 'Reglamento General de Protección de Datos']}
                
                En el caso de que no se indique por parámetro los criterios que se quieren utilizar, el sistema utilizará los criterios
                y subcriterios almacenados en el sistema. Si el sistema no tiene ninguno almacenado, muestra un mensaje de error.
                
            -csv_file_content: String. Nombre/ubicación del fichero csv que contiene los contenidos de los ficheros que se desean evaluar.
            
            -separator: String. Separador utilizado para delimitar los campos del csv indicado.
            
        Los demás parámetros consisten en parámetros de funcionamiento interno del sistema, de modo que para el uso
        de un usuario, no son relevantes.
        
        Output:
            -Lista con los resultados de la evaluación de cada documento. Cada elemento de la lista consistirá en una lista que representará
            los resultados asociados a la evaluación de un documento. Dicha lista tendrá la forma descrita en la salida del 
            método "check_document".
                        
    '''
    def multiple_executions(self, 
                            criteria=dict(),     
                            csv_file_content='',
                            separator='#',
                            
                            files_content=dict(),     #Flags de funcionamiento interno. Ignorar.
                            autoconfigure_flag=False,
                            get_found=False,
                            filtered=False,
                            clean=True
                            ):        
        
        #Vemos si utilizamos los criterios del sistema o unos externos.
        criteria=self._init_criteria(criteria)
        
        if criteria=='':
            return 'No se han especificado los criterios para realizar la evaluación.'
        
        if csv_file_content !='':
            files_content= self._rm.read_text_content_from_csv(csv_file=csv_file_content,separator=separator)

        #Filtramos
        if not filtered:
            correct_filenames, incorrect=self._rm.filter_files(files=files_content)
            
            if clean and len(incorrect)>0:
                print('Los siguientes documentos no son válidos:')
                for x in incorrect:
                    print('- ', x)
        else: 
            correct_filenames=list(files_content.keys())
            
            
        results=list()
        for filename in correct_filenames:
            results.append(self._check_criteria(criteria,
                                               files_content[filename],
                                               autoconfigure_flag=autoconfigure_flag,
                                               get_found=get_found, 
                                               clean=clean))
        return results
                    
    
    
    '''
        Autoconfigura el sistema en base a una colección de documentos y los criterios que se desea que utilice
        para realizar evaluaciones en el futuro.
        
        Esta autoconfiguración consiste tanto en el filtrado de los criterios utilizados como en 
        el ajuste de los valores umbrales idóneos para cada criterio.
        
        Input:
           -criteria: diccionario Python. Incluye, como claves, la representación de los criterios que se desean evaluar
                y como valores los subcriterios asociados a cada criterio.
            
                Por ejemplo: {'Habla de RGPD': ['RGPD', 'Reglamento General de Protección de Datos']}
                
                En el caso de que no se indique por parámetro los criterios que se quieren utilizar, el sistema utilizará los criterios
                y subcriterios almacenados en el sistema. Si el sistema no tiene ninguno almacenado, muestra un mensaje de error.
    
            -csv_file_contents: String. Ubicación/nombre del fichero csv que almacena el contenido de los documentos de la colección
            que se desea utilizar para realizar la autoconfiguración.
            
            -csv_file_evaluations: String. Ubicación/nombre del fichero csv que almacena las evaluaciones asociadas a cada documento de la
            colección que se desea utilizar para realizar la autoconfiguración.
            
            -separator: String. Separator que delimita los campos de ambos csvs introducidos. Es un único separador para ambos csvs (csv_file_contents y csv_file_evaluations)  
    '''
    def autoconfigure(self, 
                    criteria=dict(),
                    csv_file_contents='',
                    csv_file_evaluations='',
                    separator='#'       #Un único separador para
                    ):
              
        
        #Vemos si utilizamos los criterios del sistema o unos externos.
        criteria=self._init_criteria(criteria)
        
        if criteria=='':
            return 'No se han especificado los criterios para realizar la evaluación.'
    
        files_evals, files_cont=self._rm.prepare_and_filter_docs(csv_file_content=csv_file_contents,
                                                       csv_file_evaluations=csv_file_evaluations,
                                                       separator=separator)
        
        results=self.multiple_executions(criteria=criteria,
                                files_content=files_cont,
                                autoconfigure_flag=True,
                                get_found=True,
                                filtered=True,
                                clean=False)
        
        #Primero analizamos las kw útiles y extraemos las kw útiles.
        new_criteria= self._lm.analyze_kw(expected=list(files_evals.values()), 
                                          criteria=criteria,
                                          execution_results=results)
        new_results=self._rm.filter_using_criteria(results, new_criteria)
        
        self._criteria=new_criteria
        configuration['kw_threshold_value']=self._lm.get_best_kw_threshold_values(results=new_results,expected_results= list(files_evals.values())).copy()
        
        print('Sistema autoconfigurado correctamente.')
    
    '''
        MÉTODOS INTERNOS
    '''
    
    #Devuelve los criterios que utilizará el sistema en función de si los introducidos están vacíos, el sistema 
    #almacena algunos, etc.
    def _init_criteria(self,criteria_dict):
        if len(criteria_dict)==0 and self._criteria=='':
            return ''       
        
        if len(criteria_dict)==0:  
            return self._criteria.copy()
        
        return criteria_dict.copy()
    
    #Evalúa si un documento cumple con un cierto criterio.
    def _check_criteria(self,
                       criteria=dict(),
                       text='',
                       
                       autoconfigure_flag=False,  #Flags de autoconfiguración. Ignorar.
                       get_found=False,
                       clean=False
                       ):
                 
        processed_text= self._cc.pre_process_text(text)

        pos, results= 0, list()                        
        for criterion_name, subcriteria in criteria.items():               
            res=self._cc.check_criterion(pos, 
                                       subcriteria, 
                                       processed_text, 
                                       autoconfigure_flag=autoconfigure_flag,
                                       get_found=get_found)
            
            
            if clean:
                curr='OK' if res[0] else 'KO'
            else:
                if get_found:
                    curr=('OK' if res[0] else 'KO', res[1], res[2])
                else:
                    curr=('OK' if res[0] else 'KO',res[1])
                
            results.append(curr)                
            pos+=1

        return results