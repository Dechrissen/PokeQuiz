from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pokequiz",
    version="1.1.2",
    author="Derek Andersen",
    author_email="derekcandersen@gmail.com",
    description="A command line Pokemon studying tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dechrissen/PokeQuiz",
    #packages=find_packages(),
    packages=['pokequiz'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
    'console_scripts': [
        'pokequiz = pokequiz.__main__:quiz'
    ]
    },
    python_requires='>=3.6'
)
