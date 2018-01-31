from conans import ConanFile, CMake, tools
import os
import tempfile


class CpputestConan(ConanFile):
    name = "cpputest"
    version = "3.8-togs1"
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

    def fileRelativePath(self, fileName, base):
        basePath = os.path.basename(base)
        return os.path.relpath(fileName, basePath)

    def convertHeadersToRelative(self):
        includePath = 'include/'
        headerDirs = ['CppUTest', 'CppUTestExt']
        for headerDir in headerDirs:
            relativePath = os.path.join(includePath, headerDir)
            for root, dirs, files in os.walk(relativePath):
                for fileName in files:
                    headerFile = open(os.path.join(root, fileName), 'r')
                    tempHeader = tempfile.NamedTemporaryFile(mode='r+')
                    for line in headerFile:
                        wroteLine = False
                        for includeDir in headerDirs:
                            search = '#include "{}'.format(includeDir + '/')
                            includeDirectory = includeDir
                            if line.find(search) is -1:
                                continue
                            index = line.find(includeDir)
                            endIndex = line.find('"', index);
                            includeFile = line[index:endIndex]
                            relativePath = self.fileRelativePath(includeFile, root)
                            tempHeader.write(line.replace(includeFile, relativePath))
                            wroteLine = True
                        if not wroteLine:
                            tempHeader.write(line)
                    tempHeader.flush()
                    tempHeader.seek(0)
                    headerFile.close()
                    with open(os.path.join(root, fileName), 'w') as headerFile:
                        for line in tempHeader:
                            headerFile.write(line)
                    tempHeader.close()

    def package(self):
        # NOTE: This will include private headers, at this point it isn't known
        # if this will cause a problem
        self.convertHeadersToRelative()
        self.copy("*.h", dst='include/CppUTest', src='include/CppUTest');
        self.copy("*.h", dst='include/CppUTestExt', src='include/CppUTestExt');

        self.copy("*.a", dst="lib/", src="src/CppUTestExt/")
        self.copy("*.a", dst="lib/", src="src/CppUTest/")

    def package_info(self):
        self.cpp_info.libs = ["CppUTest", "CppUTestExt"]
