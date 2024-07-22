from setuptools import setup

setup(
    name='valorant-api-python',
    version='0.3',
    description='A Python Wrapper for valorant-api.com',
    author='Guimx',
    url='https://github.com/UnaPepsi/valorant-api-python',
    packages=['valorant_api_python'],
    install_requires=[
        'requests','aiohttp'
    ]
)