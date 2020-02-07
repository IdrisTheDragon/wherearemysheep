from setuptools import setup, find_packages

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description="""readme""",
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
