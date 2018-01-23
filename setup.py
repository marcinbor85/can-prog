#!/usr/bin/python

#
# The MIT License (MIT)
#
# Copyright (c) 2017 Marcin Borowicz <marcinbor85@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
from setuptools import setup

from canprog import __version__, __appname__, __description__

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        content = f.read()
    return content

setup(
    name = __appname__,
    version = __version__,
    author = "Marcin Borowicz",
    author_email = "marcinbor85@gmail.com",
    description = (__description__),
    license = "MIT",
    keywords = "bootloader socketcan can stm32",
    url = "https://github.com/marcinbor85/CAN-Prog",
    packages=['canprog', 'canprog.protocols', 'canprog.tests'],
    long_description=read('DESCRIPTION'),
    install_requires=[
        "intelhex", "python-can",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Telecommunications Industry",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
    ],
    entry_points={
          'console_scripts': [
              'canprog = canprog.main:main'
          ]
      },
)
