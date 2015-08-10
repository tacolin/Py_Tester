from target import *
import telnetlib
import time


class TelnetTarget(Target):
    def __init__(self, ip, wait_timeout=20):
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
        timeout = self.wait_timeout if timeout is None else timeout

        # for saving memory usage
        max_string_len = 0
        for string in string_tuple:
            max_string_len = len(string) if len(string) > max_string_len else max_string_len
        max_string_len *= 2

        received_list = []
        while timeout > 0.0:
            data = self.telnet.read_eager()
            if len(data) > 0:
                rx_slice = data.decode('ascii', errors='ignore')
                if len(rx_slice) > 0:
                    received_list.append(rx_slice)
                    received_string = ''.join([elem for elem in received_list])

                    # for saving memory usage
                    if len(received_string) > 2*max_string_len:
                        del received_list[0]

                    for i in range(len(string_tuple)):
                        index = received_string.find(string_tuple[i])
                        if index != -1:
                            index += len(string_tuple[i])
                            return True, i, received_string[:index]

            # check reception every 5ms
            time.sleep(0.005)
            timeout -= 0.005

        return False, -1, ''.join([elem for elem in received_list])
