# -*- coding: utf-8 -*-

'''
    Módulo de aprendizaje
    
    Contiene todas las funcionalidades asociadas al aprendizaje del sistema. Esto incluye:
        -Análisis de los criterios utilizados.
        -Autoconfiguración del sistema.
'''

class Learning_Module():
    
    
    '''
        MÉTODOS PRINCIPALES
    '''
        
    '''
        Analiza los resultados obtenidos y los criterios utilizados. A partir de esto, devuelve una nueva colección
        de criterios con los subcriterios más relevantes.
        
        Input:
            -criteria: Dict. Colección de criterios utilizados.
            -expected: List. Lista con los resultados esperados. Cada elemento de la lista es una lista con los resultados esperados para cada criterio evaluado.
            -execution_results: List. Lista con los resultados obtenidos. Cada elemento de la lista es una lista con los resultados para cada criterio. Para cada criterio, almacena:
                -porcentaje de criterios encontrados.
                -resultado con la configuración actual OK/KO (no se utiliza en el filtrado)
                -Lista con los subcriterios encontrados 
                
        Output:
            -Dict. Nueva colección de criterios con los subcriterios filtrados.
    
    '''
    def analyze_kw(self,
                   criteria=dict(),
                   expected=list(),
                   execution_results=list()
                   ):
        
        results=self._get_criteria_percentages(criteria, expected, execution_results)  #Calculamos el porcentaje de instancias positivas y negativas en las que aparece cada subcriterio de cada criterio.
        return self._filter_using_rules(criteria, results) #Extraemos los subcriterios relevantes (obviamos los que no pasan los filtros). Si, después del filtro, algún criterio se queda sin subcriterios, reestablecemos los originales.
    
    '''
        Analiza los resultados obtenidos y los esperados. En base a estos, obtiene el kw_threshold_value que genera una mayor precisión (accuracy).
        
        Input:
            -results: List. Lista con los resultados obtenidos en la ejecución previa. Cada elemento de la lista consistirá en una tupla con los resultados asociados a cada criterio.
            -expected_results: List. Lista con los resultados esperados. Cada elemento de la lista consistirá en una tupla con las evaluaciones asociadas a cada criterio de cada documento.
    '''
    def get_best_kw_threshold_values(self,
                                     results=list(),
                                     expected_results=list()
                                     ):
        
        num_crit=len(expected_results[0]) #Obtenemos el número de criterios a tratar.
        num_docs=len(results)
    
        percentages, expected= self._prepare_best_kw_value_analysis(results, expected_results, num_crit)
    
        
        thresholds=dict()
        
        for crit in range(num_crit):
            #Para cada criterio, vemos el valor de kw_treshold value que da una precisión mayor.
            best_value, best_acc=0, 0
            
            #Probamos valores entre 0 y 100.
            for value in range(101):
                acc=0                            
                for pos in range(num_docs):
                    percentage=percentages[crit][pos]*100
                    expected_value=expected[crit][pos]
                         
                    #Cálculos asociados a la accuracy
                    if percentage>=value and expected_value=='OK':
                        acc+=1
                    elif percentage < value and expected_value=='KO':
                        acc+=1   
                
                #Asociados a la accuracy
                if acc >= best_acc:
                    best_value=value
                    best_acc=acc
            
            thresholds[crit]=best_value/100         
                
        return thresholds
    
    '''
        MÉTODOS INTERNOS
    '''
    
    #Prepara las estructuras que se utilizarán para almacenar los resultados en el análisis de los criterios.
    def _prepare_kw_analysis(self, criteria):
        #Diccionario que almacenará cuantas muestras positivas y negativas hay que de cada criterio.
        pn_samples=dict() #positive/negative samples.
        for x in list(criteria.keys()):
            pn_samples[x]=dict()
            pn_samples[x]['OK']=0
            pn_samples[x]['KO']=0
            
        #Creamos un diccionario que almacenará los resultados.
        results=dict()
        results['OK']=dict()
        results['KO']=dict()
        
        for x,y in criteria.items():
            results['OK'][x]=dict()
            results['KO'][x]=dict()
            
            for z in y:
                results['OK'][x][z]=0
                results['KO'][x][z]=0
                
        return pn_samples, results
    
    #Obtiene una nueva colección de criterios filtrando los criterios que no cumplen las reglas especificadas en la documentación. 
    def _filter_using_rules(self, criteria, results):
        new_criteria= dict()
        
        ok, ko =results['OK'], results['KO']
        for crit in list(ok.keys()): #num crit
            new_criteria[crit]=list()
            for subcrit in list(results['OK'][crit].keys()):
                pos=ok[crit][subcrit]
                neg=ko[crit][subcrit]
                if (pos - neg >= 0.3 ) and neg <= 0.4 or (neg==0 and pos >0):
                    new_criteria[crit].append(subcrit)
        
        #Si algún criterio no tiene ningún elemento, pone los que había originalmente
        for crit in list(new_criteria.keys()):   
            if len(new_criteria[crit])==0:
                new_criteria[crit]= criteria[crit]
                
        return new_criteria
    
    
    #Dados los resultados esperados y los obtenidos, devuelve el porcentaje de aparición de cada subcriterio tanto para instancias positivas (OK) como instancias negativas (KO). 
    def _get_criteria_percentages(self, criteria, expected, execution_results):
        
        pn_samples, results= self._prepare_kw_analysis(criteria)       #Inicializamos las estructuras que se utilizan en el análisis para almacenar y procesar los resultados.
                
        criteria_names=list(criteria.keys())
                
        #Cálculo.
        files_pos=0        
        for x in expected:
            crit_pos=0
            for crit_answer in x:
                #crit_answer es la respuesta esperada.
                pn_samples[criteria_names[crit_pos]][crit_answer]+=1
                for z in execution_results[files_pos][crit_pos][2]:
                    results[crit_answer][criteria_names[crit_pos]][z]+=1
                crit_pos+=1
            
            files_pos+=1
        
        
        #Calculamos el porcentaje para positivos y para negativos.
        for x in list(criteria.keys()):
            for i, j in results['OK'][x].items():
                
                if pn_samples[x]['OK'] ==0:
                    results['OK'][x][i]=0
                else:
                    results['OK'][x][i]=results['OK'][x][i]/pn_samples[x]['OK']
    
    
            for i, j in results['KO'][x].items():
                
                if pn_samples[x]['KO'] ==0:
                    results['KO'][x][i]=0
                else:
                    results['KO'][x][i]=results['KO'][x][i]/pn_samples[x]['KO']
                    
        return results
    
    def _prepare_best_kw_value_analysis(self, results, expected_results, num_crit):
        percentages=dict()   #X listas. una para cada criterio.
        expected=dict()      #X listas. una para cada criterio.
        
        #Cogemos los resultados asociados a cada criterio.
        for result in results:
            for crit in range(num_crit):
                
                if not crit in percentages:
                    percentages[crit]=list()
                
                percentages[crit].append(result[crit][1])
        
        
        #Cogemos los resultados esperados asociados a cada criterio.
        for result in expected_results:
            for crit in range(num_crit):
                if not crit in expected:
                    expected[crit]=list()
                    
                expected[crit].append(result[crit])
        
        return percentages, expected