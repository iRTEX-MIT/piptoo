import json
import os.path
import os
import importlib
import sys
import tarfile
import urllib.error
from urllib.request import urlretrieve
from urllib.request import urlopen
from pprint import pprint

modules = {}

class piptoo:

    FILE = 'pip.json'
    DEP = '.pip/.dep.json'
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

        # Addons
        if not os.path.exists(self.DEP):

            STREAM = open(self.DEP, 'w+')
            STREAM.write('{}')
            STREAM.close()

    def __register__(self, package, version):

        self.PACKAGE[package] = version

    def __save__(self):

        self.STREAM = open(self.FILE, 'w+')
        self.STREAM.write(json.dumps(self.PACKAGE, indent=1))
        self.STREAM.close()

    def __use__(self, package):
        pass

    def __install__(self, package):

        try:

            with urlopen(f"https://pypi.org/pypi/{package}/json") as response:

                content = json.loads(response.read())

                if isinstance(content['releases'], object):

                    version_pkg = (list(content['releases'].keys())[-1])
                    version = content['releases'][version_pkg][-1]
                    name = content['info']['name']
                    filename = version['filename']

                    # pprint(version)

                    def report(count, blockSize, totalSize):
                        percent = int(count * blockSize * 100 / totalSize)
                        # sys.stdout.write("\r%d%%" % percent + ' complete')
                        sys.stdout.write(f"{'=':}")
                        sys.stdout.flush()

                    sys.stdout.write('\rFetching ' + version['url'] + '...\n')
                    urlretrieve(version['url'], f".pip/{filename}", reporthook=report)
                    sys.stdout.write("\rDownload complete, saved as %s" % name + '\n\n')
                    sys.stdout.flush()

                    tar = tarfile.open(f".pip/{filename}", "r:gz")
                    tar.extractall(path=f".pip/{name}")
                    tar.close()

                    if os.path.exists(f".pip/{filename}"):
                        os.remove(f".pip/{filename}")

                    os.chdir(f".pip/{name}/")
                    os.chdir(f"{os.listdir()[0]}")

                    os.system(f"python3 setup.py install")

                    if os.path.exists(f"build/lib"):
                        os.chdir(f"build/lib")
                        for path in os.listdir().reverse():
                            if os.path.exists(f"{os.listdir()[0]}/__init__.py"):
                                modules[name] = importlib.import_module(f"{path}")


                    return {
                        'version': version,
                        'version_pkg': version_pkg,
                        'name': name
                    }

                    # globals()[name] = importlib.import_module("setup.py")


        except urllib.error.HTTPError:
            return None

    def __autoloader__(self):

        if isinstance(self.PACKAGE, object):
            for package in self.PACKAGE:
                name = package
                version = self.PACKAGE[name]

                try:
                    modules[name] = importlib.import_module(name)
                except ImportError:
                    self.__install__(name)
                finally:
                    # globals()[name] = importlib.import_module(name)
                    pass

if __name__ == '__main__':
    args = sys.argv

    if '--install' in args:
        index = args.index('--install')

        if len(args) > (index + 1):

            package = args[index + 1]

            pip = piptoo()

            pip.__register__(package=package, version='last')
            pip.__save__()

            build = pip.__install__(package=package)



        else:
            print ('Package is not enter')


else:
    pip = piptoo()
    pip.__autoloader__()
