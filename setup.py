import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pokequiz",
    version="0.0.1",
    author="Derek Andersen",
    author_email="derekcandersen@gmail.com",
    description="A command line Pokemon studying tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dechrissen/PokeQuiz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
