#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net.
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-02-23
#

"""
Get a list of all languages from glosbe.com
"""

from __future__ import print_function, unicode_literals

import urllib
import re
from pprint import pprint



URL = 'http://glosbe.com/all-languages'

dict_languages = []
for match in re.findall(
        r'<a title="Dictionary .+?" href="/(\w+)/all-dictionaries">(.+?)</a>',
        urllib.urlopen(URL).read().decode('utf-8'), re.DOTALL):
    code, lang = [s.strip() for s in match]
    dict_languages.append((lang, code))



iso_langs = {}

URL = 'http://www-01.sil.org/iso639-3/codes.asp?order=639_3&letter=%25'

langsearch = re.compile(
    r"""<td>(\w\w\w)</td>\s+
    <td>.+?</td>\s+
    <td>.*?</td>\s+
    <td>(.+?)</td>""",
    re.VERBOSE | re.DOTALL).search
for row in re.findall('<tr VALIGN="TOP">(.+?)</tr>',
                      urllib.urlopen(URL).read().decode('utf-8'), re.DOTALL):
    m = langsearch(row)
    if m:
        code, lang = m.groups()
        iso_langs[lang] = code

additional_codes = []
for lang, code in dict_languages:
    if lang in iso_langs:
        iso_code = iso_langs[lang]
        if code != iso_code:  # additional code
            additional_codes.append((lang, iso_code))


dict_languages.extend(additional_codes)
dict_languages.sort()
pprint(dict_languages)
