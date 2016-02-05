
from setuptools import setup

setup(name='spatch',
      version='0.1',
      description='a ssh proxy server',
      url='https://gitlab.com/Liek0s/splatch',
      author='Pierre Jackman, Jules Baratoux',
      author_email='pierre.jackman@epitech.eu',
      license='MIT',
      packages=['splatch', 'splatchd', 'database'],
      entry_points={
          'console_scripts': [
              'splatch=splatch.__main__',
              'splatchd=splatchd.__main__'
          ]
      },
      install_requires={
          'paramiko'
      },
      zip_safe=False)
