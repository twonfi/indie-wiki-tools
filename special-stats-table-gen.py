"""Generate Special:Statistics tables to compare wikis; run as __main__"""

import requests
from json import loads
from re import match, sub
from packaging.version import Version
try:
    import pyperclip
except ModuleNotFoundError:
    auto_copy = False
else:
    auto_copy = True

try:
    email_file = open('email.txt', 'r')
except FileNotFoundError:
    raise FileNotFoundError('You must specify your email address in email.txt')
else:
    email = email_file.read()
    email_file.close()

while True:
    wikis = []

    print('\nWiki entry: Enter full URL to api.php, or wc:subdomain for Fandom')
    while True:
        wiki = input('Enter wiki'
                     f'{' or leave blank to end' if wikis else ''}: ')
        if wiki:
            if match(r'^wc:[a-z0-9-]', wiki):  # is Fandom
                wikis.append(f'https://{wiki.removeprefix('wc:')}'
                             '.fandom.com/api.php')
            else:
                wikis.append(wiki)
        else:
            break

    table = '| Stat |'

    data = {'articles': [], 'pages': [], 'files': [], 'edits': [], 'ver': []}

    for wiki in wikis:
        table += f' {sub(r'https?://|/.*', '', wiki)} |'

        r = requests.get(f'{wiki}?format=json&action=query&meta=siteinfo'
                               '&formatversion=2&siprop=general|statistics',
            headers={
            'User-Agent': 'Indie-Wiki-Tools'
                          ' +https://github.com/twonfi/indie-wiki-tools',
            'From': email
        })
        s = loads(r.text)['query']['statistics']

        data['articles'].append(s['articles'])
        data['pages'].append(s['pages'])
        data['files'].append(s['images'])
        data['edits'].append(s['edits'])
        data['ver'].append(Version(sub('^MediaWiki |-wmf.*$', '', loads(r.text)
        ['query']['general']['generator'])))


    table += '\n| --- |'
    for __ in wikis:
        table += ' --- |'

    for i in data:
        stat = data[i]
        best_stat = stat.index(max(stat))
        stat[best_stat] = f'**{stat[best_stat]}**'

    table += '\n| Content pages (articles) |'
    for i in data['articles']:
        table += f' {str(i)} |'

    table += '\n| All pages (including talk, project and redirects) |'
    for i in data['pages']:
        table += f' {str(i)} |'

    table += '\n| Files |'
    for i in data['files']:
        table += f' {str(i)} |'

    table += '\n| Edits |'
    for i in data['edits']:
        table += f' {str(i)} |'

    table += '\n| MediaWiki version |'
    for i in data['ver']:
        table += f' {str(i)} |'

    print('\n' + table)
    print('\n(Columns are in the order of entry)\n')

    if auto_copy and input('Copy to clipboard? (y/N): ').lower() == 'y':
        pyperclip.copy(table)
    if input('Another one? (y/N): ').lower() != 'y':
        break
