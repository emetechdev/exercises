# Deep Learning
**Guía:** - Qué es. - "end to end learning". - Algoritmos de Deep Learning. - Algoritmos de Machine Learning.

## Machine Learning

### Comienzos del Machine Learning
- Desde los inicios, la AI abordó y resolvió problemas intelectualmente difíciles para los humanos pero reltivamente sencillos para las computadoras.
- El reto para la AI resultó ser resolver tareas que son fáciles para los himanos pero difíciles de describir formalmente
- El **Machine Learning** es una disciplina.
- **El rendimiento de estos algoritmos de aprendizaje automático depende en gran medida de la representación de los datos que se les proporciona.**. `Ejemplo: se se usa un algoritmo de **Machine Learning** para diagnosticar a un paciente, el sistema de AI no examina al paciente directamente, en su lugr, el médico le indica al sistema varios datos relevantes, como la presencia o ausencia de determinados síntomas.`

### Qué es el Machine Learning?
El aprendizaje automático es un subdominio de la AI que proporciona a los sistemas la capacidad de aprender y mejorar automáticamente a partir de la experiencia pasada **sin ser explícitamente programados para ello.** Se basa en la hipótesis subyacente de **crear un modelo** y tratar de **mejorarlo ajustando más datos en ese modelo** a lo largo del tiempo.
Es decir, se le va  aproporcionar datos pasados y se van a ajustar de manera automática una serie de parámetros, de manera que van a poder realizar predicciones para ejemplos que no se encontraban en esa experiencia pasada tomando una determinada decisión.

### En qué consiste la creación de un Modelo?
Los componentes a más alto nivel fundamentales de una técnica de **Machine Learning** son:
- Conjunto de Datos de Entrenamiento: Se trata de la experiencia pasada.
- Algoritmo de Aprendizaje:
- Hipótesis:

                                                                     X
                                                                     ↓
|------------------|          |-------------------------|        |--------|
|Conjunto de datos |------->  |Algoritmo de aprendizaje |------> |    H   | Modelo
|de entrenamiento  |          |  (funcion hipótesis)    |        |        |
|------------------|          |-------------------------|        |--------|
                                                                     ↓
                                                                     Y (predicción)

Acá lo que hace el **Machine Learning** es 