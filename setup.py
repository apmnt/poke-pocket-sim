from setuptools import setup, find_packages

setup(
    name="poke-pocket-sim",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Aapo Montin",
    description="A Pokemon TCG Pocket Simulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/poke-pocket-sim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
