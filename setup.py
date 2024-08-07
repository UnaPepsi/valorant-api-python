from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
	name='py-valorant',
	version='1.0.2',
    description='A Python Wrapper for valorant-api.com',
	author='Guimx',
	url='https://github.com/UnaPepsi/valorant-api-python',
	install_requires=['requests','aiohttp'],
    keywords=['valorant','api','valorant-api','valorant-api.com','py-valorant'],
    license='MIT',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)