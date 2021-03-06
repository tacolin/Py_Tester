__author__ = 'Tacolin'


import unittest
import sys
sys.path.append('./testlib')
sys.path.append('./testcases')

from acCases import *
from wtpCases import *
from rpiCases import *
from telnetCases import *

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(Ac('ac_enter_linux'))
    suite.addTest(Wtp('wtp_enter_linux'))

    suite.addTest(Rpi('rpi_enable_8_network'))
    suite.addTest(Rpi('rpi_get_wtp_tarball'))
    suite.addTest(Rpi('rpi_get_ac_tarball'))
    suite.addTest(Rpi('rpi_disable_8_network'))
    suite.addTest(Rpi('rpi_enable_2_network'))

    suite.addTest(Ac('ac_get_tarball'))
    suite.addTest(Wtp('wtp_get_tarball'))

    # suite.addTest(Ac('ac_run_ac_default'))
    suite.addTest(Ac('ac_run_ac_my'))
    suite.addTest(Wtp('wtp_run_wtp_default'))

    unittest.TextTestRunner(verbosity=2).run(suite)
