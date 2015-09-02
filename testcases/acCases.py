__author__ = 'Tacolin'


from testlib import *
import unittest
import time

class Ac(unittest.TestCase):
    def setUp(self):
        self.ac = serial.SerialTarget('COM11', 115200)

    def tearDown(self):
        self.ac.disconnect()

    def ac_enter_linux(self):
        i, chk, data = 0, False, ''
        while i <= 6 and chk is not True:
            self.ac.send('cd ~')
            chk, data = self.ac.wait('root@OpenWrt:')
            i += 1
        self.assertTrue(chk, data)

        self.ac.send('killall ac')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)

    def scp_download(self, ip, username, password, remote_file, local_file):
        command = 'scp {0}@{1}:{2} {3}'.format(username, ip, remote_file, local_file)
        self.ac.send(command)

        token = "{0}@{1}'s password:".format(username, ip)
        chk, idx, data = self.ac.wait_more(['Do you want to continue connecting? (y/n)', token])
        self.assertTrue(chk, data)

        if idx == 0:
            self.ac.send('y')
            chk, data = self.ac.wait(token)
            self.assertTrue(chk, data)

        self.ac.send(password)
        chk, data = self.ac.wait('#', 60)
        self.assertTrue(chk)

    def ac_get_tarball(self):
        self.ac.send('ping -c 1 192.168.2.200')
        chk, idx, data = self.ac.wait_more(['1 packets transmitted, 1 packets received', '1 packets transmitted, 0 packets received'])
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

        self.ac.send('rm /mnt/ac_taco.tar.gz')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)

        self.scp_download('192.168.2.200', 'pi', 'raspberry', '/tftpboot/ac_taco.tar.gz', '/mnt/ac_taco.tar.gz')

        self.ac.send('tar -xzf ac_/mnt/taco.tar.gz -C /mnt/')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)

    def ac_get_vmlinux(self):
        self.ac.send('ping -c 1 192.168.2.200')
        chk, idx, data = self.ac.wait_more(['1 packets transmitted, 1 packets received', '1 packets transmitted, 0 packets received'])
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

        self.ac.send('rm /mnt/vmlinux_taco')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)

        self.scp_download('192.168.2.200', 'pi', 'raspberry', '/tftpboot/vmlinux_taco', '/mnt/vmlinux')

    def ac_reboot(self):
        self.ac.send('reboot')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)
        time.sleep(120)

    def ac_run_ac_my(self):
        self.ac.send('killall ac')
        time.sleep(2)
        self.ac.send('')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('cd /mnt/ac/')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('./ac -conf /mnt/ac/config/config.ac -set /mnt/ac/config/settings.ac.txt &')
        time.sleep(3)

        self.ac.send('')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

    def ac_run_ac_default(self):
        self.ac.send('killall ac')
        time.sleep(2)
        self.ac.send('')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('cp -f /usr/sbin/ac/config/config.ac /etc/config/capwap/config/confg.ac')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('cp -f /usr/sbin/ac/config/settings.ac.txt /etc/config/capwap/config/settings.ac.txt')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('cd /usr/sbin/ac/')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)

        self.ac.send('./ac &')
        time.sleep(2)

        self.ac.send('')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk, data)
