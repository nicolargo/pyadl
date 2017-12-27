#!/usr/bin/env python

# import os
# import sys
# import glob

from setuptools import setup

with open(os.path.join('pyadl', '__init__.py'), encoding='utf-8') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)


data_files = [
    ('share/doc/pyadl', ['AUTHORS', 'README.rst'])
]


def get_data_files():
    data_files = [
        ('share/doc/pyadl', ['AUTHORS', 'NEWS', 'README.md'])
    ]

    # if hasattr(sys, 'real_prefix') or 'bsd' in sys.platform:
    #     conf_path = os.path.join(sys.prefix, 'etc', 'glances')
    # elif not hasattr(sys, 'real_prefix') and 'linux' in sys.platform:
    #     conf_path = os.path.join('/etc', 'glances')
    # elif 'darwin' in sys.platform:
    #     conf_path = os.path.join('/usr/local', 'etc', 'glances')
    # elif 'win32' in sys.platform:
    #     conf_path = os.path.join(os.environ.get('APPDATA'), 'glances')
    # data_files.append((conf_path, ['conf/glances.conf']))

    # for mo in glob.glob('i18n/*/LC_MESSAGES/*.mo'):
    #     data_files.append((os.path.dirname(mo).replace('i18n/', 'share/locale/'), [mo]))

    return data_files


def get_requires():
    requires = []

    if sys.version_info < (2, 7):
        requires += ['argparse']

    return requires


setup(
    name='pyadl',
    version='0.1',
    description="...",
    long_description=open('README.md').read(),
    author='Nicolas Hennion',
    author_email='nicolas@nicolargo.com',
    url='https://github.com/nicolargo/pyadl',
    #download_url='https://s3.amazonaws.com/pyadl/pyadl-0.1.tar.gz',
    license="LGPL",
    keywords="...",
    install_requires=get_requires(),
    extras_require={},
    packages=['pyadl'],
    include_package_data=True,
    data_files=get_data_files(),
    # test_suite="pyadl.test",
    entry_points={"console_scripts": ["pyadl=pyadl.pyadl:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
    ]
)
