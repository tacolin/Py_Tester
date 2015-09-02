__author__ = 'Tacolin'


from testlib import *
import unittest


class Rpi(unittest.TestCase):
    def setUp(self):
        self.rpi = serial.SerialTarget('COM12', 115200)
        self.rpi.send('')
        chk, idx, data = self.rpi.wait_more(['$', 'raspberrypi login:'], 120)
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

        self.rpi.send('sudo ifdown wlan0')
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

    def scp_download(self, ip, username, password, remote_file, local_file):
        command = 'scp {0}@{1}:{2} {3}'.format(username, ip, remote_file, local_file)
        self.rpi.send(command)

        token = "{0}@{1}'s password:".format(username, ip)
        chk, idx, data = self.rpi.wait_more(['Do you want to continue connecting? (y/n)', token])
        self.assertTrue(chk, data)

        if idx == 0:
            self.rpi.send('y')
            chk, data = self.rpi.wait(token)
            self.assertTrue(chk, data)

        self.rpi.send(password)
        chk, data = self.rpi.wait('$', 60)
        self.assertTrue(chk)

    def rpi_get_wtp_tarball(self):
        self.rpi.send('rm -f ~/wtp_taco.tar.gz')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/wtp_taco.tar.gz')
        self.rpi.wait('$')

        self.scp_download('192.168.8.115', 'taco', 'taco123@', '/tftpboot/wtp_taco.tar.gz', '/tftpboot/wtp_taco.tar.gz')

        self.rpi.send('ll /tftpboot/')
        chk, idx, data = self.rpi.wait_more(['wtp_taco.tar.gz', '$'])
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

    def rpi_get_ac_vmlinux(self):
        self.rpi.send('rm -f ~/vmlinux_taco')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/vmlinux_taco')
        self.rpi.wait('$')

        self.scp_download('192.168.8.115', 'taco', 'taco123@', '/tftpboot/vmlinux_taco', '/tftpboot/vmlinux_taco')

        self.rpi.send('ll /tftpboot/')
        chk, idx, data = self.rpi.wait_more(['vmlinux_taco', '$'])
        self.assertTrue(chk, data)
        self.assertEqual(idx, 0, data)

    def rpi_get_ac_tarball(self):
        self.rpi.send('rm -f ~/ac_taco.tar.gz')
        self.rpi.wait('$')
        self.rpi.send('rm -f /tftpboot/ac_taco.tar.gz')
        self.rpi.wait('$')

        self.scp_download('192.168.8.115', 'taco', 'taco123@', '/tftpboot/ac_taco.tar.gz', '/tftpboot/ac_taco.tar.gz')

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

    def rpi_disable_2_network(self):
        self.rpi.send('sudo ifconfig eth1 down')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)

        self.rpi.send('sudo ifconfig eth1 down')
        chk, data = self.rpi.wait('$')
        self.assertTrue(chk, data)
