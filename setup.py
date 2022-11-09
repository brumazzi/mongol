from setuptools import setup
from mongol.version import FULL_VERSION as version

requirements = []
with open("requirements.txt", "r") as req:
  requirements = req.read().splitlines()

setup(
  name='mongol',
  version= version,
  description='Easy MongoDB access',
  url='github.com/brumazzi/mongol',
  author='Brumazzi',
  author_email='brumazzi_daniel@yahoo.com.br',
  license='MIT',
  packages=['mongol'],
  install_requires=requirements,
  python_requires=">=3.8.0",
  zip_safe=False
)