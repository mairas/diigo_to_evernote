Diigo to Evernote
=================

This script takes a bookmark file imported from Diigo and uploads the
bookmarks as separate formatted notes to Evernote using Evernote's REST API.

Installation
------------

Due to its simplistic nature, Diigo_to_evernote can be run in-place, assuming
that the required ``beautifulsoup4`` Python library has been installed.
Assuming a functional Python installation, ``beautifulsoup4`` can be installed
by issuing the following command::

    easy_install beautifulsoup4

Usage
-----

Diigo_to_evernote requires an Evernote developer token for operation. Get the
Evernote API key at http://dev.evernote.com/documentation/cloud/ and then
the token at http://dev.evernote.com/start/core/authentication.php#devtoken.

Copy diigo_to_evernote.conf.sample to diigo_to_evernote.conf and insert
the token. The other fields are currently not used.

Note that by default the script uses the sandbox servers only. To use
the production servers, change the sandbox parameter to ``False`` at
``diigo_to_evernote.py`` line 44.

Export your Diigo library in Delicious format. Then, issue the following
command::

    ./diigo_to_evernote.py your_diigo_bookmarks_file.html

This creates a notebook named 'Bookmarks' on your Evernote account and
uploads all your Diigo bookmarks as separate notes to that notebook.

Have fun!