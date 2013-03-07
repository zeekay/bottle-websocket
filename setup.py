from setuptools import setup

setup(
    name='bottle-websocket',
    version='0.2.5',
    author='Zach Kelling',
    author_email='zeekayy@gmail.com',
    packages=['bottle_websocket',],
    package_data={'': ['README.md']},
    description='WebSockets for bottle',
    long_description=open('README.md'),
    install_requires=['bottle', 'gevent-websocket'],
)
