
#!/usr/bin/env python
from setuptools import setup, find_packages
import os

requires = [
    'colorlog',
    "robinhood-aiokafka",
    "requests",
    "simple-settings",
    "faust",
    'splunk-sdk',
    'tabulate',
    'toml',
    'wheel',
    'flask',
    'Crypto',
    'pymongo',
    'python-magic',
    'pytz',
    'docker',
    'psutil',
    # 'aiokafka',

]

data_files = [(d, [os.path.join(d, f) for f in files])
              for d, folders, files in os.walk(os.path.join('src', 'config'))]


setup(name='kafka-sendemail',
      version='1.0',
      description='process emails using kafka',
      author='Adam Pridgen',
      author_email='adam.pridgen.phd@gmail.com',
      install_requires=requires,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
)