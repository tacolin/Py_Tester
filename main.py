__author__ = 'Tacolin'


import unittest
import sys
sys.path.append('./testlib')
sys.path.append('./testcases')


from telnetCases import *


if __name__ == '__main__':
    case1 = unittest.TestLoader().loadTestsFromTestCase(Case1)
    unittest.TextTestRunner(verbosity=2).run(case1)