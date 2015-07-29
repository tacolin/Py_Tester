__author__ = 'Tacolin'


from target import *
import telnetlib


class TelnetTarget(Target):
    def __init__(self, ip, wait_timeout=10):
        super(TelnetTarget, self).__init__()
        self.wait_timeout = wait_timeout
        self.ip = ip
        self.telnet = None
        self.connect()

    def connect(self):
        self.telnet = telnetlib.Telnet(self.ip, timeout=self.wait_timeout)

    def disconnect(self):
        self.telnet.close()
        self.telnet = None

    def write(self, string):
        self.telnet.write(string.encode('ascii'))

    def read(self, string, timeout=None):
        if timeout is None:
            return self.telnet.read_until(string.encode('ascii'), self.wait_timeout).decode('ascii')
        else:
            return self.telnet.read_until(string.encode('ascii'), timeout).decode('ascii')

    def expect(self, string_tuple, timeout=None):
        converted_list = []
        for s in string_tuple:
            converted_list.append(s.encode('ascii'))
        if timeout is None:
            expect_result = self.telnet.expect(converted_list, self.wait_timeout)
        else:
            expect_result = self.telnet.expect(converted_list, timeout)
        return expect_result[0] != -1, expect_result[0], expect_result[2].decode('ascii')
