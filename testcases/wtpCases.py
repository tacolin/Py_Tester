__author__ = 'Tacolin'


from testlib import *
import unittest
import time


class Wtp(unittest.TestCase):
    def setUp(self):
        self.wtp = serial.SerialTarget('COM10', 115200)
        self.wtp.send('')

    def tearDown(self):
        self.wtp.disconnect()

    def wtp_enter_linux(self):
        self.wtp.send('cd ~')
        chk, idx, data = self.wtp.wait_more(['ANI Enable:  1', '~#'], 120)
        self.assertTrue(chk, data)

        if idx == 0:
            chk, data = self.wtp.wait('run wtp...', 120)
            self.assertTrue(chk, data)

        self.wtp.send('cd ~')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('killall wtp')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('killall udhcpc')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

    def wtp_get_tarball(self):
        self.wtp.send('cd /tmp/')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('rm wtp_taco.tar.gz')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('tftp -g -r wtp_taco.tar.gz 192.168.2.200')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('ls')
        chk, data = self.wtp.wait('wtp_taco.tar.gz')
        self.assertTrue(chk, data)

        self.wtp.send('tar -xzf wtp_taco.tar.gz -C ./')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

    def wtp_run_wtp_default(self):
        self.wtp.send('killall wtp')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('cd /tmp/wtp/')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('./wtp &')
        time.sleep(2)
        self.wtp.send('')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)
