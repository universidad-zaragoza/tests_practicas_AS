# Tests para las prácticas de Administración de Sistemas

Este repositorio contiene tests para realizar pruebas en los scripts realizados
en las sesiones de prácticas de la asignatura de Administración de Sistemas del
grado de Ingeniería en Informática de la Universidad de Zaragoza.

## Requerimientos

Los tests requieren de un interprete de python versión 2.7 y de la biblioteca
[pexpect](https://pexpect.readthedocs.io/en/stable/).

Pexpect se puede instalar con [pip](https://pypi.org/project/pip/) ejecutando el comando:

    pip install pexpect

## Descarga y actualización de los tests

Los tests se encuentran dentro de un repositorio git y se pueden
descargar/clonar utilizando el comando:

    as@as0:~/git clone https://gitlab.unizar.es/dario/as_tests_practicas.git

Al terminar la operación se creará un directorio con todos los tests y puedes
copiarlos al directorio donde estes trabajando. Si quieres asegurarte que
tienes la última versión de los tests puedes utilizar [git
pull](https://git-scm.com/docs/git-pull) o [git
reset](https://git-scm.com/docs/git-reset) si los has modificado y no quieres
preservar las modificaciones.

    as@as0:~/as_tests_practicas/git pull origin/master

o
    as@as0:~/as_tests_practicas/git fetch --all && git reset --hard origin/master

## Utilización

El nombre de cada test es homónimo al de los scripts de los guiones de
prácticas con el prefijo test\_. Para realizar las pruebas, los tests deben
encontrarse en el mismo directorio que los scripts. Por ejemplo:

    as@as0:~/practica2/test_practica2_1.py

Cada script comprende varios tests unitarios que pueden ser ejecutados de
manera individual ya que están basados en el módulo
[unittest](https://docs.python.org/2/library/unittest.html) de python.

Cada test incluye varios tests unitarios. Cuando un test unitario se ejecuta
correctamente aparece un punto en la pantalla y si falla aparecerá un mensaje
del tipo:

    as@as0:~/practica2/test_practica2_1.py
    ......F
    ======================================================================
    FAIL: test_shebang (__main__.TestPractica2_1)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "./test_practica2_1.py", line 34, in test_shebang
          (pattern.match(first_line) != None), msg='Invalid shebang')
          AssertionError: Invalid shebang

          ----------------------------------------------------------------------
          Ran 7 tests in 0.477s

Después de `FAIL` se indica el nombre del test unitario que ha fallado, en este
caso `test_shebang` lo que nos indicará que debemos revisar la primera línea de
nuestro script. Es importante leer el nombre ya que siempre nos informára de la
parte donde ha ocurrido el error.

## Contacto

Para cualquier sugerencia de mejora, fallo, ... por favor contactar con Darío
Suárez Gracia, dario@unizar.es o @dario
