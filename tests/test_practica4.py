#!/usr/bin/env python

# WARNING!!!
# this script should be run in a chrooted environment

import os
from pexpect import pxssh
import random
import re
from subprocess import check_call
import string
import sys
from tempfile import mkstemp
import unittest

class TestPractica4(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Find script directory and store its name in a variable """
        self.my_dir=os.path.dirname(os.path.realpath(__file__))
        self.script_name=os.path.realpath('{}/../practica_4/practica_4.sh'.format(self.my_dir))
        self.IPs = ['192.168.56.2', '192.168.56.3']


    # clean before every test, just in case something goes wrong
    def setUp(self):
        self.pass_test=True

    def tearDown(self):
        pass

    def test_shebang(self):
        with open(self.script_name) as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None))

    def test_connectivity(self):
        """ Check whether the expected nodes are alive
        """

        for ip in self.IPs:
            try:
                s=pxssh.pxssh(options={"PasswordAuthentication" : "no"})
                s.login(ip, "as", ssh_key=os.path.expanduser("~/.ssh/id_as_ed25519"))
                # send inocuous command
                s.sendline('true')
                self.assertTrue(s.prompt())
                s.logout()
            except pxssh.ExceptionPxssh as e:
                self.pass_test=False
            self.assertTrue(self.pass_test, msg='Login to {} failed!, error: {}'.format(ip, e))

    def test_correct_sudo_config(self):
        """ Read sudo config file and check if root login is disabled
        """

        pattern = re.compile('^\s*PermitRootLogin\s+no')
        # remove escaped characters in case the string supports color
        rem_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        for ip in self.IPs:
            try:
                s=pxssh.pxssh(options={"PasswordAuthentication" : "no"})
                s.login(ip, "as", ssh_key=os.path.expanduser("~/.ssh/id_as_ed25519"))
                s.sendline('grep -E "^\s*PermitRootLogin\s+no" /etc/ssh/sshd_config')
                self.assertTrue(s.prompt())
                line_to_match=rem_escape.sub('', s.before.splitlines()[-1])
                self.assertTrue(pattern.match(line_to_match) != None, "Error in machine {}".format(ip))
                s.logout()
            except pxssh.ExceptionPxssh as e:
                self.pass_test=False
            self.assertTrue(self.pass_test,
                    msg='Sudo verification or login to {} failed!, error: {}, {}'.format(ip, e,s.before))

    def test_try_root_login(self):
        """ Try to login with root account
        """

        pxssh_msg=''
        login_msg=''
        for ip in self.IPs:
            valid_login=True
            try:
                s=pxssh.pxssh()
            except pxssh.ExceptionPxssh as e:
                self.pass_test=False
                pxssh_msg='pxssh {}, error: {}, {}'.format(ip, e, s.before)

            try:
                s.login(ip, "root", "toor",login_timeout=3)
            except pxssh.ExceptionPxssh as e:
                valid_login=False
                login_msg='Able to login with root to {}, error: {}, {}'.format(ip, e, s.before)

            self.assertTrue(self.pass_test, msg=pxssh_msg)
            self.assertFalse(valid_login, msg=login_msg)

if __name__ == "__main__":
    unittest.main()
