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
        i, chk, data = 0, False, ''
        while i <= 6 and chk is not True:
            self.wtp.send('cd ~')
            chk, data = self.wtp.wait('root@OpenWrt:')
            i += 1
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

    def scp_download(self, ip, username, password, remote_file, local_file):
        command = 'scp {0}@{1}:{2} {3}'.format(username, ip, remote_file, local_file)
        self.wtp.send(command)

        token = "{0}@{1}'s password:".format(username, ip)
        chk, idx, data = self.wtp.wait_more(['Do you want to continue connecting? (y/n)', token])
        self.assertTrue(chk, data)

        if idx == 0:
            self.wtp.send('y')
            chk, data = self.wtp.wait(token)
            self.assertTrue(chk, data)

        self.wtp.send(password)
        chk, data = self.wtp.wait('#', 60)
        self.assertTrue(chk)

    def wtp_get_tarball(self):
        self.wtp.send('cd /tmp/')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('rm wtp_taco.tar.gz')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.wtp.send('rm -rf /tmp/wtp/')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        self.scp_download('192.168.2.200', 'pi', 'raspberry', '/tftpboot/wtp_taco.tar.gz', '/tmp/wtp_taco.tar.gz')

        self.wtp.send('tar -xzf wtp_taco.tar.gz -C ./')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

    def wtp_run_wtp_default(self):
        self.wtp.send('killall wtp')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)

        # self.wtp.send('cd /tmp/wtp/')
        # chk, data = self.wtp.wait('#')
        # self.assertTrue(chk, data)

        # self.wtp.send('./wtp -conf /tmp/wtp/config/config.wtp &')
        self.wtp.send('wtp -conf /tmp/config.wtp &')
        time.sleep(2)
        self.wtp.send('')
        chk, data = self.wtp.wait('#')
        self.assertTrue(chk, data)
