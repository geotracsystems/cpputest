from conans import ConanFile, CMake, tools
import os


class CpputestConan(ConanFile):
    name = "cpputest"
    version = "3.5"
    license = "BSD-3"
    url = "https://github.com/geotracsystems/cpputest"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "*"

    def build(self):
        cmake = CMake(self)
        install_dir = "-DCMAKE_INSTALL_PREFIX=%s" % self.package_folder
        if self.settings.arch == "x86":
            os.environ["CFLAGS"] = "-m32"
            os.environ["CXXFLAGS"] = "-m32"
            os.environ["LDFLAGS"] = "-m32"
        self.run('cmake ./ %s %s' % (cmake.command_line, install_dir))
        self.run("cmake --build . %s" % cmake.build_config)
        self.run("make install")

    # Package step is omitted because I'm using make install to copy the
    # files to the correct location rather than trying to do it manually.

    def package_info(self):
        self.cpp_info.libs = ["CppUTest", "CppUTestExt"]
