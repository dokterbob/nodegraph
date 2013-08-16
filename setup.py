from setuptools import setup, find_packages

try:
    README = open('README.rst').read() + '\n\n'
    README += open('CHANGES.rst').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = None

setup(
    name='nodegraph',
    version='0.1',
    author='Mathijs de Bruin',
    author_email='mathijs@mathijsfiets.nl',
    packages=find_packages(),
    url='https://pypi.python.org/pypi/nodegraph/',
    description='Perspectivist graph database.',
    long_description=README,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    test_suite='nodegraph.tests'
)
