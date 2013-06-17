#!/usr/bin/env python

import os
import sys

import codecs

import ConfigParser

import cgi

import textwrap

from datetime import datetime
from collections import OrderedDict

from bs4 import BeautifulSoup

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

NOTE_TEMPLATE = textwrap.dedent(u'''\
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note>
    <h1>{title}</h1>
    <p>
    <b>URL:</b> <a href="{url}">{url}</a><br/>
    <b>Tags:</b> {tags}<br/>
    <b>Last visit:</b> {last_visit}<br/>
    <b>Add date:</b> {add_date}<br/>
    <b>Private:</b> {private}<br/>
    </p>
    </en-note>
    ''')


class EvernoteBookmarks(object):
    def __init__(self, token):
        self.token = token

        self.client = EvernoteClient(
            token=token,
            sandbox=False)

        self.user_store = self.client.get_user_store()

        version_ok = self.user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )

        if not version_ok:
            raise ValueError("Evernote API version not up to date")

        self.note_store = self.client.get_note_store()

    def list_notebooks(self):
        return self.note_store.listNotebooks()

    def create_notebook(self, notebook_name):
        notebook = Types.Notebook()
        notebook.name = notebook_name
        notebook = self.note_store.createNotebook(notebook)
        return notebook.guid

    def create_note(self, bookmark, notebook_guid):
        date_created = bookmark['add_date']*1000

        tag_string = ', '.join(bookmark['tags'])
        if 'no_tag' in tag_string:
            tag_string = ""

        content = NOTE_TEMPLATE.format(
            title=cgi.escape(bookmark['title']),
            url=cgi.escape(bookmark['url']),
            tags=cgi.escape(tag_string),
            last_visit=cgi.escape(str(datetime.fromtimestamp(bookmark['last_visit']))),
            add_date=cgi.escape(str(datetime.fromtimestamp(bookmark['add_date']))),
            private=cgi.escape("Yes" if bookmark['private'] else "No"),
        )

        note = Types.Note()
        note.title = bookmark['title'].encode('utf-8')
        note.content = content.encode('utf-8')
        note.tagNames = [bm.encode('utf-8') for bm in bookmark['tags']]
        note.created = date_created
        note.updated = date_created
        note.notebookGuid = notebook_guid

        self.note_store.createNote(note)


def get_bookmarks(html):
    soup = BeautifulSoup(html)

    anchors = soup.find_all('a')

    bookmarks = []
    for a in anchors:
        bm_data = OrderedDict()

        bm_data['title'] = a.get_text()
        bm_data['url'] = a.get('href')
        bm_data['tags'] = a.get('tags').split(',')
        bm_data['last_visit'] = int(a.get('last_visit'))
        bm_data['add_date'] = int(a.get('add_date'))
        bm_data['private'] = (a.get('private') == '1')

        bookmarks.append(bm_data)

    return bookmarks


def main():
    input_fname = sys.argv[1]

    config = ConfigParser.ConfigParser()
    config.read(('diigo_to_evernote.conf',
                os.path.expanduser(os.path.join('~', '.diigo_to_evernote.conf'))))

    # parse the input

    html = codecs.open(input_fname, 'r', 'utf-8').read()

    bookmarks = get_bookmarks(html)

    enbm = EvernoteBookmarks(config.get('Evernote', 'DeveloperToken'))

    notebooks = enbm.list_notebooks()

    try:
        notebook_guid = next(nb.guid for nb in notebooks if
                             nb.name == 'Bookmarks')
    except StopIteration:
        notebook_guid = enbm.create_notebook('Bookmarks')

    for bm in bookmarks:
        print "Adding bookmark:"
        print bm
        print ""
        enbm.create_note(bm, notebook_guid)

if __name__ == '__main__':
    main()
