"""Setup configuration for sortfiles package."""

import os
from setuptools import setup, find_packages

# Get the long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sortfiles',
    version='1.0.0',
    description='A Python application for automatically organizing and sorting files by type',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AtomicD Solutions',
    author_email='support@atomicdsolutions.com',
    url='https://github.com/atomicdsolutions/sortfiles',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[
        'flask>=2.0.0',
        'flask-socketio>=5.0.0',
        'exifread>=3.0.0',
        'pathlib>=1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'sortfiles=sortfiles.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
    keywords='file organization, sorting, automation, file management',
    project_urls={
        'Bug Reports': 'https://github.com/atomicdsolutions/sortfiles/issues',
        'Source': 'https://github.com/atomicdsolutions/sortfiles',
    },
)