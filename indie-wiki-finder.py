"""Generate Google queries; run as __main__"""

import webbrowser

while True:
    wiki_name = input('\nWiki name: ')
    search = f'%22{wiki_name}%22 (site:fandom.com | site:fextralife.com | site:neoseeker.com)'
    
    exclude = []
    while True:
        i = input('Exclude wikis (without .com) or leave blank to finish: ')
        if i:
            search += " -site:" + i + ".com"
        else:
            break
    
    print(search)
    if input('Search on Google? (y/N): ') == 'y':
        webbrowser.open('\nhttps://www.google.com/search?q=' + search + '\n')
    
    if input('Another one? (Y/n): ') == 'n':
        break
