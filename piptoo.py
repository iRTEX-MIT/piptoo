import json
import os.path
import os
import importlib
import sys
import urllib.error

from urllib.request import urlopen

class piptoo:

    ROOT = os.path.dirname(os.path.abspath(__file__))
    FILE = 'pip.json'
    PACKAGE = {}
    STREAM = False

    def __init__(self):

        # Main file
        if os.path.exists(self.FILE):

            # Project file is exists
            self.STREAM = open(self.FILE, 'r+')
            self.PACKAGE = json.loads(self.STREAM.read())
            self.STREAM.close()

        else:

            # Project file is NOT exists
            self.STREAM = open(self.FILE, 'w+')
            self.STREAM.write('{}')
            self.PACKAGE = {}
            self.STREAM.close()

    def __register__(self, package, version):

        self.PACKAGE[package] = version

    def __save__(self):

        self.STREAM = open(self.FILE, 'w+')
        self.STREAM.write(json.dumps(self.PACKAGE, indent=1))
        self.STREAM.close()

    def __use__(self, package):
        pass

    def __install__(self, package, version):

        try:

            with urlopen(f"https://pypi.org/pypi/{package}/json") as response:

                content = json.loads(response.read())

                if isinstance(content['releases'], object):
                    os.system(f"pip3 install {package}=={version}")

        except urllib.error.HTTPError:
            return None

    def __autoloader__(self):

        if isinstance(self.PACKAGE, object):
            for package in self.PACKAGE:
                name = package
                version = self.PACKAGE[name]

                try:
                    importlib.import_module(name)
                except ImportError:
                    self.__install__(name, version)
                finally:
                    # globals()[name] = importlib.import_module(name)
                    pass

if __name__ == '__main__':
    args = sys.argv

    if '--install' in args:
        index = args.index('--install')

        if len(args) > (index + 1):

            package = args[index + 1]
            name = package.split("==")[0]
            version = package.split("==")[1]

            pip = piptoo()

            build = pip.__install__(package=name, version=version)

            pip.__register__(package=name, version=version)
            pip.__save__()

        else:
            print ('Package is not enter')


else:
    pip = piptoo()
    pip.__autoloader__()
