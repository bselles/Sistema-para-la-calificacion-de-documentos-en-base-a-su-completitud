# Sistema para la calificación de documentos en base a su completitud

Trabajo de fin de máster del Máster en Ingeniería Informática del curso académico 2019/2020.

## Autor

**Gabriel Sellés** - [bselles](https://github.com/bselles)- <selles.salva.biel@gmail.com>

## Director

**Alberto Díaz** <albertodiaz@fdi.ucm.es>

## Resumen 

Debido a la constante creación de documentación en la industria, aparece la necesidad de aplicar las revisiones correspondientes para evaluar el contenido de la documentación generada. Esta labor implica un enorme esfuerzo temporal, económico y humano. Por lo tanto, es de especial interés implementar un sistema que automatice este proceso, liberando así a los profesionales de esta carga de trabajo.

Por esta razón, en este trabajo se propone un sistema que tiene la capacidad de analizar el contenido de distintos documentos y de realizar estas revisiones de forma automática. El sistema propuesto, para que sea adaptable y escalable, se ha implementado de forma que puede adaptase a distintos dominios. Su funcionamiento no se ajusta a un único tipo de documentos. 

El sistema propuesto se implementa utilizando distintas técnicas de procesamiento de lenguaje natural, de extracción de información y de aprendizaje automático. En este documento se describe tanto el funcionamiento de estas técnicas como su presencia y relevancia en la industria.

Este trabajo está relacionado con un proyecto de colaboración con la empresa ECIX Group, que plantearon esta necesidad y han proporcionado todos los recursos necesarios.


## Abstract

Due to the constant creation of documentation in the industry, there is a need to apply the corresponding revisions to evaluate the content of the documentation generated. This work implies an enormous temporary, economic, and human effort. Therefore, it is important to implement a system that automatatizes this process, thus freeing professionals from carrying out this task.
 
 
For this reason, in this project we propose a system that has the ability to analyze the content of different documents, and to realyze these reviews automatically. The proposed system, to be adaptable and scalable, has been implemented so that it can be adapted to different domains. Its operation does not conform to a single type of documents. 

The proposed system is implemented by using different Natural Language Processing, Information Extraction, and Machine Learning techniques. This document describes how these techniques work, its presence in the industry, and its relevance. 

This work is related to a collaboration project with the company ECIX Group, which raised this need, and has provided all the necessary resources. 
## Dependencias

El sistema está implementado en Python 3.6 sobre anaconda 3. Por lo tanto, para utilizar el sistema, es necesario instalar ambas plataformas y lanzar el sistema sobre ellas.

En el caso de anaconda 3, no es estrictamente necesario su uso, también se puede utilizar cualquier plataforma que permita instalar las dependencias descritas abajo. Aún así, es las pruebas realizadas se han ejecutado utilizando esta plataforma. Por lo tanto, se recomienda su uso.

Además, para utilizar las distintas funcionalidades que ofrece, el sistema emplea una serie de librerías Python que es necesario descargar e instalar. A continuación se indican los paquetes necesarios junto a los comandos que pueden usarse para descargar e instalar estas dependencias:

- nltk 3.4.4
  - complemento de stopwords de nltk: nltk.download('stopwords')
- pandas 0.24.2
- spacy 2.1.4
  - modelo de spacy en español: python -m spacy download es_core_news_sm
  - complemento para la detección de lenguajes vía spacy: pip install spacy-langdetect
- gensim 3.8.1
- word2vec 0.9.4
- rake-nltk 1.0.4
- multi-rake 0.0.1

Es importante matizar que el sistema se ha probado en Ubuntu. Por lo tanto, es posible que algunas dependencias que en linux aparecen de serie no estén en otro sistema operativo. En ese caso, será necesario descargarlase instalarlas. En los propios errores de Python aparecerían las supuestas dependencias.

Además el sistema requiere el uso de un modelo pre-entrenado vía Word2Vec. El recomendado (y el que se ha utilizado para realizar las pruebas) es el del siguiente enlance: https://www.kaggle.com/rtatman/120-million-word-spanish-corpus

También requiere un fichero .txt en el que aparezcan las stopwords que utilizará el sistema. 

Para al uso del sistema propuesto, es necesaria la configuración de los distintos parámetros del mismo. Se puede acceder a ellos en los distintos módulos (ficheros) que componen el sistema. Consisten, en su mayoría, en parámetros de construcción de instancias, de funciones, etc.