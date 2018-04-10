import os
import platform
import unittest

from conans.test.utils.tools import TestClient


class SConsTest(unittest.TestCase):

    def test_basic(self):
        if platform.system() != "Windows":
            return
        client = TestClient()
        client.runner("git clone https://github.com/memsharded/conan-scons-template .",
                      cwd=client.current_folder)
        client.run("create . user/testing")
        self.assertIn("Hello World Release!", client.out)
        client.run("create . user/testing -s build_type=Debug")
        self.assertIn("Hello World Debug!", client.out)
