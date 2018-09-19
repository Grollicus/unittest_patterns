import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unittest_patterns",
    version="0.0.1",
    author="Grollicus",
    description="Some helpers to match against complex data structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grollicus/unittest_patterns",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
