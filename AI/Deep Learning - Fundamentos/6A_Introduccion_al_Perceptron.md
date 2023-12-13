# Perceptrón
Es la evolución de la **Neurona M-P** y tiene un mejor algoritmo. Este es uno de los algoritmos más conocidos dentro del **Deep Learning** y sienta las bases de muchas de las arquitecturas de **Redes Neuronales Artificiales** de las que disponemos en la actualidad.
- Fué propuesto por Frank Rosenblatt en 1958. 

- En 1969 fue refinado y analizado por Marvin Minsky y Seymour Papert. `Marvin, M., & Seymour, A. P. (1969). Perceptrons.`

- Mejora el planteamiento de la neurona de McCulloch y Pitts añadiendo el concepto de "peso" numérico a las entradas y planteando un mecanismo para ajustarlos. 
Ej. Si recordamos el ejemplo de la primera neurona ante la pregunta "Hoy voy a ir al cine?" recibíamos una serie de inputs binarios que se correspondían a respuestas a preguntas como: si tenia tiempo hoy, si era fin de semana, etc.
En éste ejemplo nos encontramos que habían preguntas que podían tener más importancia que otras, por ejemplo si estaba abierto el cine o no.
En la **Neurona M-P** no podíamos agregar más o menos importancia a las respuestas.
Bueno, ésto es lo que mejora el **Perceptrón**, porque ya incorpora este concepto de peso (*o importancia*) y no sólo eso, sino que además plantea un mecanismo para encontrar esa importancia (*o ese valor de importancia*) de manera automática.
Y éste concepto para ajustar los pesos o importancias (*posiblemente ideales*) es lo que se conoce como **Aprender**. Es decir que sería el proceso de entrenamiento.
Por lo tanto **cuando entrenamos nuestra neurona artificial, lo que hacemos realmente es encontrar esos pesos ideales para que la neurona realice buenas predicciones. Estos pesos se denominan parámetros del modelo.**

- No recibe únicamente valores de entrada binarios, permite valores de entrada reales. 
La **Neurona M-P** sólo permitia tomar decisiónes binarias, ahora con la introducción del **Perceptrón** no sólo permite recibir valores binarios, sino que permite recibir valores dentro de un rango más amplio. También nos permite realizar predicciones que no sean una decisión binaria (*es decir que el output no sea sólo un valor binario*).

- Se basa en un tipo de neurona artificial conocida como **Threshold Logic Unit (TLU)**
Hay que aclarar que el **Perceptron** no es un algoritmo que se base en una única neurona artificial como la **Neurona M-P**, sino que consiste en un algoritmo que está constituido por varias neuronas artificiales y cada una de éstas se denomina **Threshold Logic UNIT**.
Esto quiere decir que en nuestra arquitectura, nuestro perceptron puede estar formado por varias neuronas.
Por ejemplo, si en nuestra arquitectura, nuestro perceptron puede estar formado por varias neuronas que llamaremos en el ejemplo gráfico **TW**, y si tenemos varios inputs (x1, x2, x3). Estos inputs entrarán a las diferentes neuronas y las diferentes neuronas nos proporcionarán diferentes resultados que tendremos que interpretar.
Es decir el **Perceptron** tal y como lo vemos **es una arquitectura de Red Neuronal Artificial** y que no tiene porque estar formado por una única neurona y las neuronas que lo forman se denominan **TLU - Threshold Logic Unit**.
![Esquema de TLU](img/6_esquema_de_TLU.png)

- La TLU computa una **suma parametrizada** de las entradas.

## Neurona M-P vs Perceptrón (TLU)
En el gráfico se muestra una **Neurona M-P** que para repasar su funcionamientos se puede ir a la docu `"5A_RNA_Red_Neuronal_Artificial.md"`. Ahora si quisiéramos complejizarla y agregar valor a algunas de las preguntas del ejercicio.
Por ejemplo, si la pregunta de si "es fin de semana?" es importante (por si tenemos tareas que realizar, donde si es un viernes o un sábado podríamos tener un día más para realizar la tarea), con este ejemplo lo que buscamos es que esa pregunta, o ese valor de la variable **X1** de si *es fin de semana?*, tenga un **peso mayor** que si *estrenan pelicula?* (porque da igual que estrene pelicula, si tengo tarea que realizar y si no es fin de semana porque voy a tener que entregar la tarea y tengo que hacerla). Bueno, aquí es donde se incorpora el concepto de **importancia o peso** mencionado para el **Perceptron**.
Entonces, éste peso, en el ejemplo va a venir marcado con **W1, W2, y W3** y cada uno de los valores de entrada (*x1, x2, y x3*), van a tener asociado un peso, de manera que se puede establecer ese peso para que esas variables de entrada valgan más o valgan menos.
Por ejemplo, si yo quiero que *fin de semana?* valga más, le asigno un peso mayor que al resto de variables. En éste caso, puedo decir que **W1** sea igual a 2, mientras que el peso del resto de variables sea 1.
Ahora la **función Z** ya no va a ser una **agregación** (una suma de todas las entradas), sino que va a ser una suma parametrizada en base a esos pesos.

Todo este cálculo se ve a la derecha en el gráfico, escrito con verde y rojo.
En el ejemplo se vio como lo calcularíamos de forma manual, pero la diferencia fundamental entre la **TLU** que forma el **Perceptrón** y la **Neurona M-P** es que éstos pesos no se elijen de manera manual. 
Es decir, vamos a usar un algoritmo que va a seleccionar éstos pesos de manera automática en base a **Experiencia pasada**.
Cómo lo hacemos?
Agarramos las últimas 20 veces que fuimos al cine, extraemos estas 3 preguntas de esas 20 veces que fuimos al cine. Entonces extraemos las respuestas (si/no) de las preguntas de la experiencia de las ultimas 20 veces pasadas, y con ésto formamos una tabla que llamaremos **Conjunto de Datos** y estará formada por ésas características de entrada, de la experiencia pasada y la variable de salida, es decir "si fuimos o no".

![Neurona vs Perceptrón](img/6_neurona_vs_perceptron.png)

Entonces, lo que hacemos es tomar un **Conjunto de experiencias pasadas** se lo proporcionamos a nuestro algoritmo y en base a estos datos pasados, el algoritmo de manera autónoma va a ser capaz de identificar estos pesos, la importanci que tiene cada una de esas variables de entrada o cada una de esas preguntas para nosotros en particular.

## Perceptrón y eliminación del Threshold
La diferencia entre la **Neurona M-P** y el **Perceptron**  no se limita a los pesos y a la forma de aprenderlos de manera automática, sino que también trata de mejorar el concepto de **Threshold**, ya que anteriormente el **Threshold** se definia de forma manual, ahora se intenta calcularlo a partir de **Experiencia pasada**.
Entonces se empieza a considerar al **Threshold** como una improtancia más, es decir como un peso más para una característica que va a ser igual a uno.
Entones, se crea una **nueva caracterísitca de entrada, X0**, que siempre va a ser igual a uno y que va a tener asociado como peso el **Threshold**, de manera que ese mismo algoritmo que usábamos para ajustar el valor de la importancia de los pesos **W1, W2, y W3** de manera automática, tambien sirva para seleccionar ese **Threshold** de manera automática en base a esa experiencia pasada.
Entonces la funcion de agregacion (la verde) donde se multiplicaba las "X" con las "W" y se sumaban, va a cambiar y la sumatoria de Z, desde x1 a xn, va a ser ahora la sumatoria desde x0 a xn. Donde "X0" va a ser siempre 1.
De ésta forma la **función a** también cambia.
Hay que aclarar que en la literatura éste nuevo **Threshold** que es el **X0** se lo va a encontrar como **BIAS** (*se lo denomina como término de prejuicio o parcialidad*).
**BIAS** se lo denomina como término de prejuicio o parcialidad porque de manera intuitiva éste término establece ese concepto de parcialidad entre, por ejemplo, una persona que le guste muchísimo el cine entonces este **Bias o nuevo threshold** va a ser muy pequeño porque las probabilidades de ir al cine van a ser mayores, y ésto lo va a aprender de la experiencia pasada. En cambio a alguien que le importa poco ir al cine, el **bias** le va a salir alto porque quizas para que vaya necesite que se le alineen todos los planetas, la luna esté en júpiter, que tenga ganas, plata, que vaya obligado entre otras "casualidades" que lo obliguen a ir al cine.
Entonces este **bias** va a ser clave para juzgar en la decisión.

![Bias](img/6_bias.png)

## Threshold Logic Unit (TLU)
- La TLU computa una **suma parametrizada** de entradas. Esto es porque le multiplicamos el peso de la característica de entrada.

- Después, aplica una **función de activación** sobre la suma calculada anteriormente.

En el gráfico **b** es el **Bias**.
![TLU](img/6_TLU.png)

## Notación y funcionamiento del Perceptrón
A tener en cuenta:
El **Perceptrón** se corresponde con una arquitectura compuesta por **una única capa de TLUs**.
Permite la clasificación de instancias en diferentes clases binarias de manera simultánea.
En el gráfico de ejemplo (de la izquierda) tenemos un **Perceptrón** que recibe 2 características de entrada **x1 y x2**, tenemos 3 **TLU's** que formarían parte de esa única capa. Hay que tener en cuenta que si buscamos en internet, hay literatura en las que los autores refieren a ésta arquitectura como si fuera una única TLU.
Pero la forma más comunmente aceptada es referirse a **Perceptrón** como esta arquitectura que puede tener varias TLU's en una única capa, sin embargo, que no sorprenda si en algún momento hay referencia a ellas como **una arquitectura con una capa de una única TLU**.
**En el gráfico de la derecha se ve cómo funciona una única TLU**, ahora el problema es que tenemos un perceptrón que tiene una capa con 3 TLU's con lo cual de alguna manera tenemos que diferenciar entre los parámetros (con los pesos) de cada una de las TLU's. Como convención en la notación, en éste caso que vemos a la derecha (el perceptrón de una única TLU), tenemos 3 pesos (w1, w2, b) y éstos pesos se suelen denominar como **parámetros del modelo**, entonces tendríamos 3 parámetros del modelo para éste perceptrón de una única TLU.
Recordar que se denomina **Modelo** a **todo el conjunto de ecuaciónes que forman parte de ésta arquitectura (en éste caso Perceptrón)**.
Una vez que hemos ajustado esos pesos (o parámetros w1, w2 y b), veremos que el resultado hw(x) quedaría parametrizado por los parámetros.

![Arquitectura con varias TLU's](img/6_arq_con_varias_TLUs.png)

Cuando hablamos de un perceptrón con varias TLU's, la cosa cambia.
Tendríamos las características de entradas x1, x2 y b=1, éstas conformarían **una capa denominada "Input Layer"** (pintada de amarillo).
La capa conformada con las 3 TLU's se denomina **Output Layer (es la última capa que nos proporciona los resultados)**, es importante recordar ésta notación porque se usa en arquitecturas más complejas donde hay capas intermedias (que en éste ejemplo no se ven).
Es importante saber que en éste caso vamos a tener más de un resultado donde cada TLU nos va a proporcionar de manera independiente cada una, un resultado diferente, en consecuencia podrémos denominar esos resultados como **Hw(x)1=y1, Hw(x)2=y2 y Hw(x)3=y3**.
Una vez que tenemos la notación general, veremos cómo se desarrollan cada una de las fórmulas de éstas TLU's en base a los pesos.
Cada una de éstas variables de entrada (x1, x2 y b) ya no solo se introducen en una única TLU, sino que e introduce en 3 TLU's, lo que significa que cada una de las características de entrada tendrá asociado un peso para cada una de las TLU's.
También tendremos para cada TLU una función de agregación "Z" y una de activación "A".

![Funcionamiento de perceptron](img/6_funcionamiento_de_perceptron.png)

De ésta forma tendríamos en lugar de 3 parámetros del modelo con 3 pesos, en la fórmula completa tendríamos 9 parámetros (o pesos, en el gráfico está marcado con rosa) y tendríamos que encargarnos de encontrar los valores de todos ellos de manera que la predicción final fuera adecuada.
Aspectos relevantes a tener en cuenta:
- Cada una de éstas neuronas que vemos aquí (es decir, cada TLU) nos va a proporcionar un resultado de manera independiente.

![Ejemplo de input para deteccion de mails](img/6_ejemplo_deteccion_de_spam.png)

Para los resultados que arroje cada TLU, es decir cada "y", se pueden aplicar diferentes sistemas para llegar a una conclusión final. Por ejemplo se puede aplicar un sistema de clasificación por voto y decir que "el número que más se repita, va a ser mi resultado final", en el ejemplo, el resultado final es cero, es decir, es un correo legítimo.

Otra de las cosas interesantes que permiten realizar el perceptrón teniendo varias TLU's en la **capa de salida, en la "Output Layer"**, es que **nos permite realizar clasificación multi clase en lugar de clasificación binaria**.
La **Clasificación multiclase** se basa en los siguiente:
Imaginemos que tenemos un problema que queremos resolver, en el que en lugar de tener únicamente 2 categorías de salida como en el ejemplo de "deteccion de spams" que serían "legítimo" y "spam", pero si tuvieramos 3 categorías por ejemplo, quedaría como: *categoría 1, categoría 2 y categoría 3*.
En un escenario así, se podría usar éste algortimo para que realice una clasificación entre las 3 ctegorías. Esto se haría codificando o representando cada categoría de la sigueinte forma: 
- *Categoría 1* = [1, 0, 0]
- *Categoría 2* = [0, 1, 0]
- *Categoría 3* = [0, 0, 1]

Ahora, para saber cómo acierta mi algoritmo, se hace de la siguiente forma:
Imaginemos que tengo una predicción en la que el algoritmo me dice por ejemplo:
en la primera TLU me da 0, la segunda tambien pero la tercera me da 1.
Enteonces, tomo esos 3 resultados, los trato como un vector (en el ejemplo queda como [0, 0, 1]). Y lo que tendré será que mi perceptrón me está prediciendo que en función de éstas características de entrada que le proporcionamos y el valor que tienen éstos pesos del modelo, en base a lo que yo lo entrené con mi conjunto de datos de entrenamiento. Lo que me va a decir es que para ése ejemplo nuevo, el que le pasa a las caraacterísticas de entrada, se corresponde con la categoría 3.

![Clasificacion Multiclase](img/6_clasificacion_multiclase.png)