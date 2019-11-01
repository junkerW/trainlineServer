from setuptools import setup

setup(
   name='bahn',
   version='0.1',
   description='Bahn finder',
   author='Sebastian',
   author_email='sebastian.wenzel@gmx.net',
   packages=['bahn'],  #same as name
   install_requires=['Flask', 'trainline'], #external packages as dependencies
)