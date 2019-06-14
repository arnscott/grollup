from setuptools import setup

version = '0.0.01'

namespace_packages = []

packages = ['grollup']

scripts = ['bin/ghostrollup']

install_requires = []

setup(name='ghostrollup',
      version=version,
      namespace_packages=namespace_packages,
      packages=packages,
      scripts=scripts,
      license='open',
      author='Aaron Scott',
      author_email='aa5278sc-s@student.lu.se',
      install_requires=install_requires)