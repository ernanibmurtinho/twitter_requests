from setuptools import find_namespace_packages, setup

packages = [package for package in find_namespace_packages(include=['twitter_ingestion', 'twitter_ingestion.*'])]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='twitter_ingestion',
    version='1.0.0',
    author='Ernani de Britto Murtinho',
    author_email='ernanibmurtinho@gmail.com',
    description='TWITTER_INGESTION: Job for retrieve data from twitter',
    long_description=long_description,
    python_requires='>=3.7',
    platforms='MacOS X; Linux',
    packages=packages,
    install_requires=(
        'pex',
    ),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
