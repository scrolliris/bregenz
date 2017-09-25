# pylint: disable=C0103
"""Bregenz setup script
"""

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, *('doc', 'README.rst'))) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGELOG')) as f:
    CHANGES = f.read()

requires = [
    'beaker',
    'bleach',
    'colorlog',
    'markdown',
    'Paste',
    'PasteScript',
    'python-dotenv',
    'pyramid',
    'pyramid_assetviews',
    'pyramid_beaker',
    'pyramid_mako',
    'PyYAML',
    'webob',
    'wsgi-basic-auth',
]

if sys.version_info[0] < 3:  # python 2.7
    requires.extend([
        'ipaddress',
        'typing',
        'pytz',
    ])

development_requires = [
    'pylibmc',
    'better_exceptions',
    'flake8',
    'flake8_docstrings',
    'pylint',
    'waitress',
]

testing_requires = [
    'python-memcached',
    'better_exceptions',
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'WebTest',
]

production_requires = [
    'CherryPy',
]

setup(
    name='bregenz',
    version='0.0.1',
    description='bregenz',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'development': development_requires,
        'testing': testing_requires,
        'production': production_requires,
    },
    install_requires=requires,
    message_extractors={'bregenz': [
        ('**.py', 'python', None),
        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
        ('static/**', 'ignore', None),
    ]},
    entry_points="""\
    [paste.app_factory]
    main = bregenz:main
    [console_scripts]
    bregenz_pserve = bregenz.scripts.pserve:main
    bregenz_pstart = bregenz.scripts.pstart:main
    """,
)
