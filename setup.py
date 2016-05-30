#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='GroupCurses',
    version='0.1.0-alpha',
    description='A terminal interface to the GroupMe platform.',
    long_description=long_description,
    url='https://github.com/aetherith/groupcurses',
    author='Thomas C. Foulds',
    author_email='thomas.foulds@aetherith.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='chat GroupMe messaging',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'urwid',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'groupcurses=groupcurses:main',    
        ]  
    },
)
