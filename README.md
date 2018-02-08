# Tests para las prácticas de Administración de Sistemas

Este repositorio contiene tests para realizar pruebas en los scripts realizados
en las sesiones de prácticas de la asignatura de Administración de Sistemas del
grado de Ingeniería en Informática de la Universidad de Zaragoza.

## Requerimientos

Los tests requieren de un interprete de python y de la biblioteca
[pexpect](https://pexpect.readthedocs.io/en/stable/).

## Utilización

El nombre de cada test es homónimo al de los scripts de los guiones de
prácticas con el prefijo test\_. Para realizar las pruebas, los tests deben
encontrarse en el mismo directorio que los scripts. Por ejemplo:

    as@as0:~/practica2/test_practica2_1.py

Cada script comprende varios tests unitarios que pueden ser ejecutados de
manera individual ya que están basados en el módulo
[unittest](https://docs.python.org/2/library/unittest.html) de python.

## Contacto

Para cualquier sugerencia de mejora, fallo, ... por favor contactar con Darío
Suárez Gracia, dario@unizar.es o @dario
