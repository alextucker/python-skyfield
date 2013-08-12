from distutils.core import setup, Command

import skyfield  # to learn the version

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='skyfield',
    version=skyfield.__version__,
    description=skyfield.__doc__,
    long_description=open('README.rst').read(),
    license='MIT',
    author='Brandon Rhodes',
    author_email='brandon@rhodesmill.org',
    url='http://github.com/brandon-rhodes/python-skyfield/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Astronomy',
        ],
    packages=[ 'skyfield', 'skyfield.tests' ],
    package_data = {'skyfield': ['documentation/*.rst']},
    install_requires=['de421==2008', 'jplephem', 'numpy', 'sgp4'],
    cmdclass = {'test': PyTest},
    )
