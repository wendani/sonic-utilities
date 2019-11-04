import os
import sys
from click.testing import CliRunner
from unittest import TestCase
import subprocess

import show.main as show

root_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(root_path)
scripts_path = os.path.join(modules_path, "scripts")

class TestIntfutil(TestCase):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["PATH"] += os.pathsep + scripts_path
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def setUp(self):
        self.runner = CliRunner()

    # Test 'show interfaces status' / 'intfutil status'
    def test_intf_status(self):
        # Test 'show interfaces status'
        result = self.runner.invoke(show.cli.commands["interfaces"].commands["status"], [])
        print >> sys.stderr, result.output
        expected_output = (
              "Interface    Lanes    Speed    MTU      Alias    Vlan    Oper    Admin             Type    Asym PFC\n"
            "-----------  -------  -------  -----  ---------  ------  ------  -------  ---------------  ----------\n"
            "  Ethernet0        0      25G   9100  Ethernet0  routed    down       up  QSFP28 or later         off"
        )
        self.assertEqual(result.output.strip(), expected_output)

        # Test 'intfutil status'
        output = subprocess.check_output('intfutil status', stderr=subprocess.STDOUT, shell=True)
        print >> sys.stderr, output
        self.assertEqual(output.strip(), expected_output)

    # Test 'show interfaces status --verbose'
    def test_intf_status_verbose(self):
        result = self.runner.invoke(show.cli.commands["interfaces"].commands["status"], ["--verbose"])
        print >> sys.stderr, result.output
        expected_output = "Command: intfutil status"
        self.assertEqual(result.output.split('\n')[0], expected_output)
        assert(0)

    @classmethod
    def teardown_class(cls):
        print("TEARDOWN")
        os.environ["PATH"] = os.pathsep.join(os.environ["PATH"].split(os.pathsep)[:-1])
        os.environ["UTILITIES_UNIT_TESTING"] = "0"
