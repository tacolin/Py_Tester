__author__ = 'Tacolin'


from testlib import *
import unittest


class Rpi(unittest.TestCase):
    def setUp(self):
        self.rpi = serial.SerialTarget('COM12', 115200)
        self.rpi.send('')
        chk, idx, data = self.rpi.wait_more(['$', 'raspberrypi login:'])
        self.assertTrue(chk, data)
        self.assertTrue(idx in [0, 1], data)

        if idx == 0:
            pass
        elif idx == 1:
            self.rpi.send('pi')
            chk, data = self.rpi.wait('Password:')
            self.assertTrue(chk, data)

            self.rpi.send('raspberry')
            chk, data = self.rpi.wait('$')
            self.assertTrue(chk, data)

    def tearDown(self):
        self.rpi.disconnect()

    def rpi_enable_8_network(self):
        self.rpi.send('sudo ifconfig eth0 192.168.8.7 netmask 255.255.255.0')
        self.rpi.wait('$')

        self.rpi.send('ping -c 1 192.168.8.115')
        chk, idx, data = self.rpi.wait_more(['1 packets transmitted, 1 received', '1 packets transmitted, 0 received'])
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

    def rpi_get_wtp_tarball(self):
        self.rpi.send('rm -f ~/wtp_taco.tar.gz')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/wtp_taco.tar.gz')
        self.rpi.wait('$')

        self.rpi.send('tftp -v 192.168.8.115 -c get wtp_taco.tar.gz')
        chk, idx, data = self.rpi.wait_more(['$', 'Error code'], 60)
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

        self.rpi.send('mv ~/wtp_taco.tar.gz /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('ll /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)
        self.assertTrue('wtp_taco.tar.gz' in data, data)

    def rpi_get_ac_vmlinux(self):
        self.rpi.send('rm -f ~/vmlinux_taco')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/vmlinux_taco')
        self.rpi.wait('$')

        self.rpi.send('tftp -v 192.168.8.115 -c get vmlinux_taco')
        chk, idx, data = self.rpi.wait_more(['$', 'Error code'], 200)
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

        self.rpi.send('mv ~/vmlinux_taco /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('ll /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)
        self.assertTrue('vmlinux_taco' in data, data)

    def rpi_get_ac_tarball(self):
        self.rpi.send('rm -f ~/ac_taco.tar.gz')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/ac_taco.tar.gz')
        self.rpi.wait('$')

        self.rpi.send('tftp -v 192.168.8.115 -c get ac_taco.tar.gz')
        chk, idx, data = self.rpi.wait_more(['$', 'Error code'], 60)
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

        self.rpi.send('mv ~/ac_taco.tar.gz /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('ll /tftpboot/')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)
        self.assertTrue('ac_taco.tar.gz' in data, data)

    def rpi_disable_8_network(self):
        self.rpi.send('sudo ifconfig eth0 down')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('sudo ifconfig eth0 down')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

    def rpi_enable_2_network(self):
        self.rpi.send('sudo ifconfig eth1 192.168.2.200 netmask 255.255.0')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('sudo ifconfig eth1 192.168.2.200 netmask 255.255.0')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)
