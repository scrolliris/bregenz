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
    'markdown',
    'Paste',
    'PasteScript',
    'python-dotenv',
    'pyramid',
    'pyramid_assetviews',
    'pyramid_beaker',
    'pyramid_mako',
    'pyramid_secure_response',
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
    'colorlog',
    'better_exceptions',
    'pylibmc',
    'waitress',

    'flake8',
    'flake8_docstrings',
    'pydocstyle',
    'pycodestyle',
    'pyflakes',
    'pylint',
]

testing_requires = [
    'colorlog',
    'better_exceptions',
    'python-memcached',

    'flake8',
    'flake8_docstrings',
    'pydocstyle',
    'pycodestyle',
    'pyflakes',
    'pylint',

    'pytest',
    'pytest-cov',
    'pytest-mock',
    'WebTest',
]

production_requires = [
    'CherryPy',
]

setup(
    name='willisau',
    version='0.0.1',
    description='willisau',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
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
    entry_points="""\
    [paste.app_factory]
    main = willisau:main
    [console_scripts]
    willisau_pserve = willisau.scripts.pserve:main
    willisau_pstart = willisau.scripts.pstart:main
    """,
)
