__author__ = 'Tacolin'


from testlib import *
import unittest


class Case1(unittest.TestCase):
    def setUp(self):
        self.tel = telnet.TelnetTarget('192.168.8.5')
        self.username = 'mme'
        self.password = 'mme'

        chk, data = self.tel.wait('login:')
        self.assertEqual(chk, True, data)

        self.tel.send(self.username)
        chk, data = self.tel.wait('Password:')
        self.assertEqual(chk, True, data)

        self.tel.send(self.password)
        chk, data = self.tel.wait('$')
        self.assertEqual(chk, True, data)

    def tearDown(self):
        self.tel.disconnect()

    def test_update(self):
        self.tel.send('sudo apt-get update')
        chk, idx, data = self.tel.wait_more(['password for mme:', '$'], 60)
        self.assertEqual(chk, True, data)
        self.assertTrue(idx in [0, 1], data)

        if idx == 0:
            self.tel.send(self.password)
            chk, data = self.tel.wait('$', 60)
            self.assertEqual(chk, True, data)

    def test_upgrade(self):
        self.tel.send('sudo apt-get upgrade -y')
        chk, idx, data = self.tel.wait_more(['password for mme:', '$'], 60)
        self.assertEqual(chk, True, data)
        self.assertTrue(idx in [0, 1], data)

        if idx == 0:
            self.tel.send(self.password)
            chk, data = self.tel.wait('$', 60)
            self.assertEqual(chk, True, data)
