import platform

from conan_tests.test_regression.utils.base_exe import BaseExeTest, run
from conans.tools import save


class CMakeStdTest(BaseExeTest):

    def cmake_with_raw_flag_test(self):

        conanfile = """from conans import ConanFile, CMake
import os
class Conan(ConanFile):
    name = "lib"
    version = "1.0"
    settings = "os", "compiler", "arch", "build_type", "cppstd"
    exports_sources = "*"
    build_requires = "cmake_installer/2.8.12@conan/stable"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

"""

        test_main = """#include <iostream>

int main() {
    auto a = 1;
}
"""
        cmake = """
project(MyHello CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(main main.cpp)
"""
        save("conanfile.py", conanfile)
        save("main.cpp", test_main)
        save("CMakeLists.txt", cmake)
        if platform.system() == "Windows":
            settings = '-s compiler="Visual Studio" -s compiler.version=14'  # cmake 2.8 doesn't work with 15
        else:
            settings = ""
        out = run("conan create . user/channel -s cppstd=14 %s" % settings, capture=True)
        self.assertIn("Conan setting CXX_FLAGS flags: -std=c++14", out)
