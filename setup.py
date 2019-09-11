import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-nsfw-python3",
    version="0.0.5",
    author="Danilo Silva de Oliveira",
    author_email="danilooliveira28@hotmail.com",
    description="A useful package to detect sexual content based on yahoo's open_nsfw.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ds-oliveira/open_nsfw_python3",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.16.4',
        'image>=1.5.27',
    ],
    package_data={
        'open_nsfw_python3': ['*.caffemodel', '*.prototxt', '*.md'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires='>=3.6',
)
