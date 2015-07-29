__author__ = 'Tacolin'


from target import *
import serial


class SerialTarget(Target):
    def __init__(self, port, baudrate=9600, wait_timeout=10, parity=serial.PARITY_NONE, rtscts=False, xonxoff=False, dsrdtr=False):
        super(SerialTarget, self).__init__()
        self.serial = None
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.rtscts = rtscts
        self.xonxoff = xonxoff
        self.dsrdtr = dsrdtr
        self.wait_timeout = wait_timeout
        self.connect()

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, parity=self.parity, timeout=0.1, rtscts=self.rtscts, dsrdtr=self.dsrdtr)

    def disconnect(self):
        self.serial.close()
        self.serial = None

    def write(self, string):
        self.serial.write(string.encode('ascii'))

    def readall(self):
        while True:
            buffer_size = self.serial.inWaiting()
            if buffer_size > 0:
                return self.serial.read(buffer_size).decode('ascii')
            sleep(0.005)

    def read(self, string, timeout=None):
        timeout = self.wait_timeout if timeout is None else timeout
        received_list = []
        while timeout > 0.0:
            buffer_size = self.serial.inWaiting()
            if buffer_size > 0:
                received_list.append(self.serial.read(buffer_size).decode('ascii'))
                received_string = ''.join([elem for elem in received_list])
                index = received_string.find(string)
                if index != -1:
                    index += len(string)
                    return received_string[:index]
            sleep(0.005)
            timeout -= 0.005
        return ''.join([elem for elem in received_list])

    def expect(self, string_tuple, timeout=None):
        timeout = self.wait_timeout if timeout is None else timeout
        received_list = []
        while timeout > 0.0:
            buffer_size = self.serial.inWaiting()
            if buffer_size > 0:
                received_list.append(self.serial.read(buffer_size).decode('ascii'))
                received_string = ''.join([elem for elem in received_list])
                for i in range(len(string_tuple)):
                    index = received_string.find(string_tuple[i])
                    if index != -1:
                        index += len(string_tuple[i])
                        return True, i, received_string[:index]
            sleep(0.005)
            timeout -= 0.005
        return False, -1, ''.join([elem for elem in received_list])

# if __name__ == '__main__':
#     import sys
#     ser = SerialTarget('COM7', 115200, 1)
#     while True:
#         # data = ser.readall()
#         # data = ser.read('tacolin')
#         chk, idx, data = ser.expect(('tacolin', 'potegrant'))
#         if len(data) > 0:
#             sys.stdout.write(data)
