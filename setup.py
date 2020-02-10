import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EDAAudioSync",
    version="0.1.3",
    author="Jeremy Grifski",
    author_email="grifski.1@osu.edu",
    description="A tool for syncing audio and EDA data during an interview",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrg94/EDAAudioSync",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'data_sync = tools.data_sync:main',
            'data_aggregate = tools.data_aggregator:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'pyaudio',
        'matplotlib'
    ],
)