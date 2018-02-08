#!/usr/bin/env python

import os
import pexpect
import random
import re
from shutil import rmtree
import string
import sys
from tempfile import mkstemp, mkdtemp
import unittest

class TestPractica2_5(unittest.TestCase):

    def setUp(self):
        """ Nothing to setup """

    def tearDown(self):
        """ Nothing to finish """

    def test_shebang(self):
        with open('./practica2_5.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or 
                    (pattern.match(first_line) != None))

    def test_no_dir(self):
        invalid_dir_name=''.join([ random.choice(string.ascii_letters+string.digits+' ') for _ in range(128) ])
        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_5.sh')
            self.child.expect('Introduzca el nombre de un directorio: ')
            self.child.sendline(invalid_dir_name)
            self.child.expect('{} no es un directorio'.format(invalid_dir_name))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

    def test_empty_dir(self):
        tmp_dir_name = mkdtemp(prefix=' with spaces ')

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_5.sh')
            self.child.expect('Introduzca el nombre de un directorio: ')
            self.child.sendline(tmp_dir_name)
            self.child.expect('El numero de ficheros y directorios en {} es de 0 y 0, respectivamente'.format(tmp_dir_name))
        except:
            self.assertTrue(False)
        self.assertTrue(True)

        os.rmdir(tmp_dir_name)
        self.child.terminate(force=True)


    def test_regular_case(self):
        # create a random number of directories 
        tmp_dir_name = mkdtemp(prefix=' with spaces ')

        n_dirs=random.randint(1, 16)
        n_files=random.randint(1, 256)

        list_dirs= [ mkdtemp(dir=tmp_dir_name) for _ in range(n_dirs) ] + [ tmp_dir_name ]

        for _ in range(n_files):
            mkstemp(dir=random.choice(list_dirs), prefix=' louis pouzin')

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_5.sh')
            self.child.expect('Introduzca el nombre de un directorio: ')
            self.child.sendline(tmp_dir_name)
            self.child.expect('El numero de ficheros y directorios en {} es de {} y {}, respectivamente'.format(tmp_dir_name, n_dirs, n_files))
        except:
            self.assertTrue(False)
        self.assertTrue(True)

        rmtree(tmp_dir_name)
        self.child.terminate(force=True)
    

if __name__ == "__main__":
    unittest.main()
