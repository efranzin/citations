# `citations.py`

**Usage:**

`citations.py [-b BAI] [-y Y] [-l LATESTYEARS] [-c COLLECTION] [--lessauthors] [-r]`

**Options:**
* `-b BAI, --BAI BAI`, specifies the author's BAI identifier
* `-y Y, --year Y`, results for a given year
* `-l LATESTYEARS, --latestyears LATESTYEARS`, results for the latest given years
* `-c COLLECTION, --collection COLLECTION`, collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis
* `--lessauthors`, limit the results to publications with 10 authors or less
* `-r, --reversed`, sorts the items in chronological order

Default values are `E.Franzin.1` for the BAI, `article` for the collection and all the corresponding items in the Inspirehep database are sorted from the most recent.
