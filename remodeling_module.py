# -*- coding: utf-8 -*-

'''
    Módulo de acondicionamiento de las colecciones utilizadas
    
    Es el encargado de analizar la información introducida por el usuario respecto a colecciones y evaluaciones para luego procesarla y acomodarla a un 
    formato que los demás componentes del sistema puedan utilizar. 
    
    Además, es el encargado de filtrar los documentos no válidos.
    
    Los documentos no válidos son aquellos que son muy cortos (de forma predeterminada, aquellos documentos con menos de 50 términos) o que no están en español.
    
'''

from utilities import configuration

class Remodeling_Module():

    def __init__(self, 
                 text_analyzer=''
                 ):
        
        self._text_analyzer=text_analyzer
        
        
        
    '''
        MÉTODOS PRINCIPALES
    '''
    '''
        Filtra y acondiciona la entrada introducida por el usuario.
        
        Lee los csvs introducidos y genera estructuras adecuadas para que los demás componentes del sistema utilicen la información introducida 
        por el usuario.
        
        Además, informa (a través de mensajes por pantalla) cuando algún documento de la colección no es válido.
        
        Input:
            -csv_file_content: String. Ubicación del fichero csv que incluye el contenido de los documentos a utilizar.
            -csv_file_evaluation: String. Ubicación del fichero csv que incluye las evaluaciones asociadas a los documentos a utilizar.
            -separator: String. Símbolo que sirve de separador dentro de los ficheros csv.
            
        Output:
            -files_evals: Dict. Diccionario cuyas claves son los nombres de los ficheros y los valores las evaluaciones asociadas a cada criterio.
            -files_cont: Dict. Diccionario cuyas claves son los nombres de los ficheros y los valores son el contenido del propio documento.
    '''
    
    #devuelve dos diccionarios. Ambos tienen como clave los nombres de los docs. 
    #Como valores, uno tiene las evaluaciones y otro es el contenido del documento.
    def prepare_and_filter_docs(self,
                                csv_file_content='',
                                csv_file_evaluations='',
                                separator=';'
                               ):
        
        #dict. claves: nombres de los docs. valores: evaluaciones (lista de OK/KO) por criterio.
        files_evaluations= self._read_csv_files_evaluations(csv_file=csv_file_evaluations,
                                         separator=separator)
        
        
        #dict. claves: nombres de los docs. valores: contenido del texto.
        files_contents= self.read_text_content_from_csv(csv_file=csv_file_content, separator=separator)
           
        #Mezclamos el contenido de ambos. Atendemos principalmente a los docs de las evaluaciones.
        files=dict()
        for x in files_evaluations.keys():
            files[x]=files_contents[x]
                
        #filtramos los documentos.
        correct=self._filter_unvalid_files(files=files)
        
        files_evals=dict()
        files_cont=dict()
        
        for x in correct:
            files_evals[x]=files_evaluations[x].copy()
            files_cont[x]=files_contents[x]
        
        return files_evals, files_cont
    
    '''
        Dado un texto, evalúa si es válido.
        
        Un documento es válido si su tamaño es mayor que 50 términos (parámetro configurable) y
        si está en español.
        
        Input:
            -text: String. Texto a evaluar.
            
        Output:
            -Boolean. True si es válido. False si no.
    '''
    def check_text_validity(self,text):
        size=0
        words=''
            
        paragraphs=text.split('\n')
        for x in paragraphs:
            for y in x.split():
                size+=1
                words+=y+' '
                
                if size == configuration['min_text_size'] and self._check_language(words.lower()):
                    return True
         
        return False
    
    '''
        Obtiene los resultados obtenidos si hubiesemos aplicado una colección filtrada de criterios.
        
        Este método se utiliza exclusivamente en la funcionalidad de autoconfiguración del sistema.
        
        Input:
            -results: Dict. resultados obtenidos en la ejecución (y resultados que queremos filtrar).
            -new_criteria: Dict. nueva colección de criterios utilizada
            
        Output:
            -List: resultados filtrados en base a los nuevos criterios.
        
    '''
    def filter_using_criteria(self, results, new_criteria):
        num_crit=len(results[0]) #Obtenemos el número de criterios a tratar.
        num_docs=len(results)
        
        criteria_keys=list(new_criteria.keys())
        
        filtered_results=list()
        
        for doc in range(num_docs):
            new_doc=list()
            
            for crit in range(num_crit):
                subcr_found=results[doc][crit][2]
                found=0
            
                for x in subcr_found:
                    if x in new_criteria[criteria_keys[crit]]:
                        found+=1
                    
                new_doc.append(('OK',found/len(new_criteria[criteria_keys[crit]])))
            
            filtered_results.append(new_doc)
                
        
        return filtered_results
        
    #Devuelve dos listas con los NOMBRES de los docs correctos y los incorrectos.
    def filter_files(self,
                       files=dict()
                       ):
        correct=list()
        incorrect=list()
        
        for filename, filecontent in files.items():
            
            if self.check_text_validity(filecontent):
                correct.append(filename)
            else:
                incorrect.append(filename)
                
        return correct, incorrect
    
    #Lee el contenido de los textos a partir del csv correspondiente.
    #Presupone que el contenido del csv incluye una cabecera.
    def read_text_content_from_csv(self,csv_file='', separator=''):
        with open(csv_file, 'r', encoding='latin-1') as f:
            csv_content=f.read()
            
        result=dict() #Diccionario cuyas claves serán el nombre del fichero y el valor será el contenido del mismo.
        files= csv_content.split('\n')
        files.pop(0) #Eliminamos la cabecera
        
        for file in files:            
            fields= file.split(separator)
    
            if len(fields) > 1: #Si no es una línea vacía (la última).
                result[fields[2]]=fields[3]
    
        return result           
    
    
    '''
        MÉTODOS SECUNDARIOS
    '''
    
    #Lee el csv de las evaluaciones asociadas a los documentos.
    def _read_csv_files_evaluations(self,
                         csv_file='',
                         header=True,
                         encoding='latin-1', 
                         separator='#',
                         source_dir=''
                         ):
        
        with open(csv_file, 'r', encoding='latin-1') as f:
            content=f.read()
            
        #Variable en la que se volcarán los resultados
        files=dict()
        
        lines=content.split('\n')
        #Eliminamos la última línea porque está vacía.
        lines.pop()
        
        if not header:
            #Obtenemos el número de criterios.
            num_crit= len(lines[0].split(separator))
            
            #Insertamos el valor de la primera línea (posición 0)
            line_content=lines[0].split(separator)
            results=list()
            for x in range(1,num_crit):
                results.append(line_content[x])
            
            filepath= line_content[0] if source_dir == '' else source_dir+'/'+line_content[0]
            files[filepath]=results
        
        else:
            #Obtenemos el número de criterios.
            num_crit= len(lines[1].split(separator))
       
    
        #Insertamos los elementos del csv en el resultado.
        for x in range(1, len(lines)):
            line_content=lines[x].split(separator)
            
            results=list()
            for x in range(1,num_crit):
                results.append(line_content[x])
            
            filepath= line_content[0] if source_dir == '' else source_dir+'/'+line_content[0]
            
            files[filepath]=results 
        
        return files    

        
        
    #Devuelve si el lenguaje del texto es el adecuado (español).
    def _check_language(self,text):
        res=self._text_analyzer.detect_language(text)
        return res =='es'
    
    #files: diccionario cuyas claves son los nombres de los ficheros y los valores su contenido.    
    #Devuelve una lista con los nombres de los documentos correctos. Contiene los NOMBRES de los CORRECTOS.
    def _filter_unvalid_files(self,
                             files=dict()
                             ):
        correct, incorrect =self.filter_files(files=files)
                
        if len(incorrect)!=0:
            print('Los siguientes documentos no son válidos:')
    
            for x in incorrect:
                print('-'+ x)
        
        return correct    