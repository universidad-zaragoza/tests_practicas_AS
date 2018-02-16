#!/usr/bin/env python

import os
import pexpect
import random
import re
from shutil import rmtree
from stat import S_IXUSR
import string
import sys
import unittest

class TestPractica2_6(unittest.TestCase):

    def setUp(self):
        self.home=os.getenv("HOME")

    def tearDown(self):
        """ Nothing to finish """

    def test_shebang(self):
        with open('./practica2_6.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or 
                    (pattern.match(first_line) != None))
        
    # helper function
    def is_exe(self, fname):
        fstats=os.stat(fname)
        return fstats.st_mode & S_IXUSR

    def find_bin_dir(self):
        """ Find the directory bin\w\w\w that is the least frequency modified

            Returns a tuple with a boolean value and a directory name
        """

        home=self.home
        pattern=re.compile('bin\w\w\w')
        candidate_dirs=[ os.path.abspath(home + '/' + d) for d in os.listdir(home) if os.path.isdir(os.path.abspath(home + '/' + d)) and pattern.match(d) ]
        # return the least recently modified directory
        if len(candidate_dirs) == 0: 
            return True, ""
        else:
            return False, sorted(candidate_dirs, key=lambda d: os.stat(d).st_mtime)[0]



    def test_existing_dir(self):

        # if there is no bin_dir, we create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        if bin_dir_required:
            bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            while os.path.isdir(bin_dir):
                bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            # directory creation
            os.mkdir(bin_dir)

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_exe(f) ]

        read_exec_files=[]

        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_6.sh')
#            self.child.logfile = sys.stdout
            if bin_dir_required:
                reg_exp='Se ha creado el directorio {}/(bin\w\w\w)'.format(self.home)
                match=self.child.expect(reg_exp)
                bin_dir=os.path.abspath(self.home + '/' + self.child.match.group(1))
        except:
            self.assertTrue(False)

        try:
            self.child.expect('Directorio destino de copia: {}'.format(bin_dir))
            second_bin_dir=self.child.match.group().split()[-1]
            self.assertTrue(second_bin_dir == bin_dir)
        except:
            print str(self.child)
            self.assertTrue(False)

        try:
            for _ in exec_files:
                reg_exp='(.*) ha sido copiado a {}\r\n'.format(bin_dir)
                self.child.expect(reg_exp)
                read_exec_files.append(os.path.basename(self.child.match.group(1).split()[-1]))
            self.child.expect('Se han copiado {} archivos'.format(str(len(exec_files))))
            # check whether all files have been copied
            self.assertTrue(set(exec_files) == set(read_exec_files))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)
        rmtree(bin_dir)
        


    def test_dir_creation(self):

        # if there is no bin_dir, the script should create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        # remove the directory if it exists, to ensure the creation by the script
        if not bin_dir_required:
            rmtree(bin_dir)

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_exe(f) ]

        read_exec_files=[]

        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_6.sh')
#            self.child.logfile = sys.stdout
            if bin_dir_required:
                reg_exp='Se ha creado el directorio {}/(bin\w\w\w)'.format(self.home)
                match=self.child.expect(reg_exp)
                bin_dir=os.path.abspath(self.home + '/' + self.child.match.group(1))
        except:
            self.assertTrue(False)

        try:
            self.child.expect('Directorio destino de copia: {}'.format(bin_dir))
            second_bin_dir=self.child.match.group().split()[-1]
            self.assertTrue(second_bin_dir == bin_dir)
        except:
            print str(self.child)
            self.assertTrue(False)

        try:
            for _ in exec_files:
                reg_exp='(.*) ha sido copiado a {}\r\n'.format(bin_dir)
                self.child.expect(reg_exp)
                read_exec_files.append(os.path.basename(self.child.match.group(1).split()[-1]))
            self.child.expect('Se han copiado {} archivos'.format(str(len(exec_files))))
            # check whether all files have been copied
            self.assertTrue(set(exec_files) == set(read_exec_files))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

if __name__ == "__main__":
    unittest.main()
