from setuptools import setup, find_packages

# FIXME: this might not work!

setup(
    name="diigo_to_evernote",
    version="1.0.0",
    packages=find_packages(),

    install_requires=['beautifulsoup4'],

    # metadata for upload to PyPI
    author="Matti Airas",
    author_email="mairas@iki.fi",
    description="A minimal script to upload bookmarks exported from Diigo to Evernote",
    license="MIT",
    keywords="Diigo Evernote transfer convert script",
    url="https://github.com/mairas/diigo_to_evernote",

    entry_points = {
        'console_scripts': [
            'diigo_to_evernote = diigo_to_evernote:main',
        ],
    }
)
