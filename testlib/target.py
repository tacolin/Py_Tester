__author__ = 'Tacolin'


from abc import ABCMeta, abstractmethod


class Target(metaclass=ABCMeta):
    def __init__(self):
        super(Target, self).__init__()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def write(self, string):
        pass

    @abstractmethod
    def read(self, string, timeout=None):
        pass

    @abstractmethod
    def expect(self, string_list, timeout=None):
        return 0

    def send(self, string):
        self.write('%s\n' % string)

    def wait(self, string, timeout=None):
        rx_data = self.read(string, timeout)
        if string in rx_data:
            return True, rx_data
        else:
            return False, rx_data

    def wait_more(self, string_set, timeout=None):
        return self.expect(string_set, timeout)
