import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = unicode(open(os.path.join(here, 'README.rst')).read(), 'utf-8')
CHANGES = unicode(open(os.path.join(here, 'CHANGES.rst')).read(), 'utf-8')
versionfile = open(os.path.join(here, "nodules", "_version.py")).read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in nodules/_version.py.")

requires = [
    'nodular',
    ]

dependency_links = [
    'https://github.com/hasgeek/nodular/archive/master.zip#egg=nodular'
    ]


setup(
    name='nodules',
    version=version,
    description='Revisioned content objects',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        ],
    author='Kiran Jonnalagadda',
    author_email='kiran@hasgeek.com',
    url='https://github.com/hasgeek/nodules',
    keywords=['nodules', 'nodular'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='tests',
    install_requires=requires,
    dependency_links=dependency_links,
    )
