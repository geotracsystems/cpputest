from conans import ConanFile, CMake, tools
import os
import re


class CpputestConan(ConanFile):
    name = "cpputest"
    version = "3.5-1"
    license = "BSD-3"
    url = "https://github.com/geotracsystems/cpputest"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "*"

    def build(self):
        cmake = CMake(self)
        if self.settings.arch == "x86":
            os.environ["CFLAGS"] = "-m32"
            os.environ["CXXFLAGS"] = "-m32"
            os.environ["LDFLAGS"] = "-m32"
        os.environ["CFLAGS"] += " -g"
        os.environ["CXXFLAGS"] += " -g"
        self.run('cmake ./ %s' % (cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        # NOTE: This will include private headers, at this point it isn't known
        # if this will cause a problem
        self.copy("*.h", dst='include/CppUTest', src='include/CppUTest');
        self.copy("*.h", dst='include/CppUTestExt', src='include/CppUTestExt');

        self.copy("*.a", dst="lib/", src="src/CppUTestExt/")
        self.copy("*.a", dst="lib/", src="src/CppUTest/")

    def package_info(self):
        self.cpp_info.libs = ["CppUTest", "CppUTestExt"]
