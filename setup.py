from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chatpywork',
    version='1.0.0',
    descrption='python wrapper for ChatWork API v2',
    long_description=long_description,
    url='https://github.com/tannakaken/chatpywork',
    author='tannakaken',
    author_email='tannakaken@gmail.com',
    license='MIT',
    install_requires=['requests'],
    keywords='chatwork',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
)
