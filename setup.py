from setuptools import setup
from os import path

readme = open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read()

setup(
    name='bottle-websocket',
    version='0.2',
    author='Zach Kelling',
    author_email='zeekayy@gmail.com',
    packages=['bottle_websocket',],
    description='WebSockets for bottle',
    long_description=readme,
    install_requires=['bottle', 'gevent-websocket'],
)
