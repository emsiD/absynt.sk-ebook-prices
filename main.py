from operator import itemgetter
from urllib import request
import re

# The original idea was to simply list all the book names here and then transform them into path names
# however, not all of them follow the convention, as some already are in their second edition (url suffix -2)
# and even worse, there is "Smrť v bunkri" on "/mrtvy-v-bunkri", which made me go for
# pulling the title from the page as well.
urls = ["cista-biela-rasa",
        "vsetky-larine-vojny",
        "vesmir-v-kvapke-vody",
        "chladnokrvne",
        "laserovy-muz",
        "slon-na-zempline",
        "posledni-svedkovia",
        "vyluceni",
        "1947",
        "dve-sestry",
        "eli-eli",
        "cisar",
        "mrtvy-v-bunkri",
        "tancujuce-medvede",
        "jeden-z-nas-paperback",
        "najdem-si-ta",
        "devat-zivotov",
        "casy-zo-second-handu-2",
        "planeta-kaukaz",
        "pol-potov-usmev",
        "roztrateni-nemci",
        "vrah-z-mesta-marhul",
        "cernobylska-modlitba",
        "vojna-nema-zensku-tvar-1",
        "kolymske-denniky",
        "vsetci-mocni-kremla",
        "sachinsach",
        "zinkovi-chlapci",
        "vlcice-zo-sernovodska-1",
        "vitajte-v-raji-1",
        "eben",
        "nocni-putnici",
        "americky-cisar",
        "casy-zo-second-handu-1",
        "papusa",
        "imperium",
        "vojna-nema-zensku-tvar",
        "sce-ne-vmerla-i-ne-vmre",
        "a-vo-viedenskom-lese-stale-stoja-stromy",
        "cigan-je-cigan",
        "akoby-si-kamen-jedla",
        "oci-zasypane-pieskom-1"]

booklist = []

# removing whitespace makes it easier to find the price among all the tabs and newlines
translations = str.maketrans("", "", '\t\n\r\v\f')

# this tag only appears twice on the page - before both prices
price_clue = '<span class="price" itemprop="price">'
title_clue = '<h1 class="product-name" itemprop="name">'

for suffix in urls:
    url = 'https://www.absynt.sk/'+ suffix
    u = request.urlopen(url)
    record = []
    # removing whitespace here to make 'clue' nice and simple to maintain
    response_string = u.read().decode().translate(translations)
    price_pattern = re.compile(price_clue.translate(translations))
    title_pattern = re.compile(title_clue.translate(translations))

    # The desired information lays just after the clue.
    # We find the relevant index and scan the page
    # until we hit the delimiter, "<" for title, "€" for prices
    title_start_index = title_pattern.search(response_string).end()
    title = response_string[title_start_index:].partition("<")[0]
    record.append(title)
    # e-book is the second price on the page, hence an iterator is used
    for link in price_pattern.finditer(response_string):
        price_string = response_string[link.end():].partition("€")[0]
        price = float(price_string.replace(",","."))
        record.append(price)
    booklist.append(record)
    print("Got information for {}...".format(title))

# apparently faster than a lambda would be
booklist = sorted(booklist, key=itemgetter(2))

for book in booklist:
    print("E-book: {:5.2f}€ Paper: {:5.2f}€ {}".format(book[2], book[1], book[0]))
