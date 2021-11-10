#Cache

Este git corresponde al Proyecto 3: Cache del curso IE0521 Estructuras de computadoras digitales II de la Escuela de Ingeniería Eléctrica de la Universidad de Costa Rica.

Está realizado en el I Semestre del 2020 por:
-Sofía Fonseca Muñoz, carné B42634
-Freddy Zúñiga Cerdas, carné A45967
-Jeffry Luque, carné B33893
-Guillermo González, carné B53080

Se diseño un cache en python3 para sistemas opertivos Linux. El tamaño, el tamaño de linea de cache y la asociatividad son configurables. Utiliza la politica de reemplazo LRU con ___ como optimizacion avanzada.

--------------
Instrucciones:
--------------

Para ejecutar el programa, se debe contar con Python3. El programa correrá bajo la siguiente instrucción:

gunzip -c branch-trace-gcc.trace.gz | cache -s <#> -l <#> -a <#>

Donde cada uno de los parámetros corresponden de la siguiente manera:

	s: Tamaño de cache. Configurable de 32 a 128 KB.
  
  l: Tamaño de linea de cache: configurable de 32 a 128 B.
  
  a: Asociatividad: configurable de 4 a 16 ways.
