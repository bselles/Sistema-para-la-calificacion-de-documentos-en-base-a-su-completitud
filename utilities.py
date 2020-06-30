# -*- coding: utf-8 -*-


'''
    Módulo de utilidades
    
    Incluye múltiples métodos auxiliares utilizados por el sistema.
    
    También incluye la configuración compartida por parte del sistema implementado.
    
'''

'''
    Valores predeterminados de configuración del sistema
'''
configuration=dict()

configuration['configuration_file']=''
configuration['threshold_value']=
configuration['kw_threshold_value']={}   
configuration['default_threshold']=
configuration['min_text_size']=
        


'''
    Lee el contenido de un fichero y lo devuelve.
    
    Input:
        -filename: String. Ubicación del fichero a leer.
        -encoding: String. Codificación utilizada en la lectura.

    Output:
        -String. Contenido del fichero.
'''
def read_file(filename, encoding='latin-1'):

    with open(filename, "r", encoding=encoding) as myfile:
        return myfile.read()    
    
'''
    Lee los criterios (y subcriterios) asociados a un fichero de criterios.

    Input:
        -filepath: String. Ubicación/nombre del fichero de criterios.
        -encoding: String. Codificación utilizada en la lectura.
    Output:
        -Dict. Diccionario cuyas claves son los criterios leídos y los valores listas con los subcriterios asociados a cada criterio.
'''
def read_criteria(filepath, encoding='latin-1'):
    result={} #Diccionario en el que se volcarán los resultados.
    #Leemos la totalidad del texto.
    text=read_file(filepath, encoding=encoding) 
        
    text=text.split('--')[1:] #Eliminamos el elemento vacío que se ubica en la primera posición.
    
    #Para cada criterio, obtenemos los subcriterios/palabras clave e insertamos 
    #lo obtenido en el diccionario resultante.    
    for x in text:
        tmp=x.split('**')
        key=tmp[0].strip('\n')
        values=list()
        
        for y in tmp[1:]:
            values.append(y.strip('\n'))
        
        result[key]=values
        
    return result