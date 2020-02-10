from setuptools import setup, find_packages

setup(
    name='wheresmysheep',
    version='0.1.0',
    description='wheres my sheep using opencv & libtiff',
    long_description="""readme""",
    author='Nathan Williams',
    author_email='nathaniwilliamsuk@gmail.com',
    url='https://github.com/idristhedragon/wheresmysheep',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
