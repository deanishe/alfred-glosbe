#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net.
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-02-23
#

"""translate.py [options] <source> <dest> <query>

Ask Glosbe.com to translate <query> from language <source> to language <dest>

<source> and <dest> languages should be specifed in 3-letter ISO 639-3 format,
although many 2-letter codes (en, de, fr) will work.

See http://en.wikipedia.org/wiki/List_of_ISO_639-3_codes for full list.

Usage:
    translate.py <source> <dest> <query>
    translate.py [-t | --text] (-l | --langs) [<query>]
    translate.py (-h | --help)
    translate.py --openhelp

Options:
    -l, --langs     Display list of languages
    -t, --text      Output text, not Alfred XML
    -h, --help      Display this help message
    --openhelp      Open the workflow help file in your browser

"""

from __future__ import print_function, unicode_literals

import os
import sys
import hashlib
import urllib
import subprocess
from HTMLParser import HTMLParser
from workflow import Workflow, web, ICON_ERROR, ICON_WARNING


log = None

API_URL = 'http://glosbe.com/gapi_v0_1/translate'

# For unescaping HTML escape codes
unescape = HTMLParser().unescape


def search_api(wf, source, dest, query):
    """Search the Glosbe.com API"""
    params = {'from': source, 'dest': dest,
              'phrase': query, 'format': 'json',
              'pretty': 'true'
              }
    log.debug('Calling %s with args : %r', API_URL, params)
    r = web.get(API_URL, params=params)
    if r.error:
        wf.add_item('Error contacting Glosbe.com',
                    r.reason, valid=False, icon=ICON_ERROR)
        wf.send_feedback()
        return 0
    results = r.json()
    translations = []
    for result in results.get('tuc', []):
        translation = result.get('phrase', {}).get('text', '')
        if not translation:
            continue
        log.debug('translation : %r', translation)
        meanings = []
        for meaning in result.get('meanings', []):
            text = meaning.get('text', '')
            language = meaning.get('language', '')
            if not text or language != dest:
                continue
            log.debug('  → meaning : %s', text)
            meanings.append(text)
        if not len(meanings):
            translations.append((unescape(translation), ''))
        else:
            for meaning in meanings:
                translations.append((unescape(translation), unescape(meaning)))
    return translations


def open_help_file():
    """Open the included help file"""
    path = os.path.join(os.path.dirname(__file__), 'Help.html')
    subprocess.call(['open', path])


def filter_langs(query):
    """Return only languages matching query"""
    from languages import LANGS
    if not query:
        return [pair for pair in LANGS if len(pair[1]) == 3]
    langs = []
    query = query.lower()
    for lang, code in LANGS:
        if len(code) != 3:
            continue
        if query in lang.lower() or query in code.lower():
            langs.append((lang, code))
    return langs


def output_langs(wf, langs, text_output=False):
    """Print languages to STDOUT as Alfred XML or text"""
    if text_output:  # CLI output
        longest = len(max([t[0] for t in langs], key=len))
        for lang, code in langs:
            fmt = '{{0:<{}}}   {{1}}'.format(longest)
            print(fmt.format(lang, code).encode('utf-8'))
    else:  # Alfred XML
        if not len(langs):
            wf.add_item("No languages found", valid=False, icon=ICON_WARNING)
        else:
            for lang, code in langs:
                wf.add_item(lang, code, uid=code, arg=code,
                            valid=True, icon='icon.png')
        wf.send_feedback()


def main(wf):
    import docopt
    global log
    log = wf.logger
    log.debug('script args : %s', wf.args)
    args = docopt.docopt(__doc__, argv=wf.args)
    log.debug('docopt args : %s', args)
    query = args.get('<query>', '')
    text_output = args.get('--text', False)
    if args.get('--openhelp'):
        open_help_file()
        return 0
    elif args.get('--langs'):
        output_langs(wf, filter_langs(query), text_output)
        return 0
    elif not query:  # Can't do anything without a query
        return 0

    # Query web API
    # Check that languages are valid
    from languages import LANGS
    codes = [p[1] for p in LANGS]
    source = args.get('<source>')
    dest = args.get('<dest>')
    err = False
    if source not in codes:
        wf.add_item('Unknown source language : {0}'.format(source),
                    '', valid=False, icon=ICON_ERROR)
        err = True
    if dest not in codes:
        wf.add_item('Unknown destination language : {0}'.format(dest),
                    '', valid=False, icon=ICON_ERROR)
        err = True
    if err:
        wf.send_feedback()
        return 0

    def wrapper():
        return search_api(wf, source, dest, query)

    key = '{}-{}-{}'.format(source, dest, query).encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    url = b'http://glosbe.com/{0}/{1}/{2}'.format(
        source, dest,
        urllib.quote(query.encode('utf-8')))

    results = wf.cached_data(key, wrapper, max_age=600)

    with open(wf.cachefile('url'), 'wb') as file:
        file.write(url)

    if not len(results):
        wf.add_item("No translations for '{0}'".format(query),
                    valid=False,
                    icon=ICON_WARNING)
    else:
        for translation, definition in results:
            wf.add_item(translation, definition, arg=translation,
                        valid=True, icon='icon.png')
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
