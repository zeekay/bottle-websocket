from setuptools import setup

setup(
    name='bottle-websocket',
    version='0.2',
    author='Zach Kelling',
    author_email='zeekayy@gmail.com',
    packages=['bottle_websocket',],
    description='WebSockets for bottle',
    long_description=open('README.md').read(),
    install_requires=['bottle', 'gevent-websocket'],
)
