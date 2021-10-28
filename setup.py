from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='encoded-video',
    packages=find_packages(exclude=['examples']),
    version='0.0.2',
    # license=, # TODO - codebase heavily draws from pytorchvideo. need to issue license correctly.
    description='Video utilities',
    author='Nathan Raw',
    author_email='naterawdata@gmail.com',
    url='https://github.com/nateraw/encoded-video',
    install_requires=requirements,
)
