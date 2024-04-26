import codecs

from setuptools import find_packages, setup

# Read the contents of your README file
with codecs.open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

# Read the contents of your requirements file
with codecs.open('requirements.txt', encoding='utf-8') as fh:
    requirements = fh.read().splitlines()

setup(
    name='motorAnyio',
    version='0.1.0',
    author='obnoxious',
    author_email='obnoxious@dongcorp.org',
    description='A anyio port of motor that only supports asyncio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/obnoxiousish/async_twitter_api_client',
    packages=['motorAnyio'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: AsyncIO',
    ],
    python_requires='>=3.7',
)
