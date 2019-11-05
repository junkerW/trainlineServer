from setuptools import setup

setup(
   name='bahn',
   version='0.2',
   description='Bahn finder',
   author='Sebastian',
   author_email='sebastian.wenzel@gmx.net',
   packages=['bahn'],  #same as name
   install_requires=[
      'Flask',
      'trainline@git+https://github.com/junkerW/trainline-python.git',
      'json2html'
      ],  #external packages as dependencies
   include_package_data=True
)
