from setuptools import find_packages, setup

setup(
    name='encoded-video',
    packages=find_packages(exclude=['examples']),
    version='0.0.3',
    # license=, # TODO - codebase heavily draws from pytorchvideo. need to issue license correctly.
    description='Video utilities',
    author='Nathan Raw',
    author_email='naterawdata@gmail.com',
    url='https://github.com/nateraw/encoded-video',
    install_requires=[
        "av>=14.0.1",
        "iopath",
        "numpy",
    ]
)
