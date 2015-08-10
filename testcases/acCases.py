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
        self.ac.send('cd ~')
        chk, data = self.ac.wait('root@OpenWrt:~#')
        self.assertTrue(chk, data)

        self.ac.send('killall ac')
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

        self.ac.send('scp pi@192.168.2.200:/tftpboot/vmlinux_taco ./mnt/vmlinux')
        chk, idx, data = self.ac.wait_more(['Do you want to continue connecting? (y/n)', "pi@192.168.2.200's password:"])
        self.assertTrue(chk, data)

        if idx == 0:
            self.ac.send('y')
            chk, data = self.ac.wait("pi@192.168.2.200's password:")
            self.assertTrue(chk, data)

        self.ac.send('raspberry')
        chk, data = self.ac.wait('#', 30)
        self.assertTrue(chk)

    def ac_reboot(self):
        self.ac.send('reboot')
        chk, data = self.ac.wait('#')
        self.assertTrue(chk)
        time.sleep(120)

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
