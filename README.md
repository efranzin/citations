# `citations.py`

**Usage:**

`citations.py [-b BAI] [-y GIVEN_YEAR | -l LATEST_YEARS] [-c COLLECTION] [-a NUMBER_OF_AUTHORS] [-r]`

**Options:**
* `-b/--BAI BAI`, specifies the author's BAI identifier
* `-y/--year GIVEN_YEAR`, results for a given year, e.g. 2020
* `-l/--latest LATEST_YEARS`, results for the latest given years, e.g. 5
* `-c/--collection COLLECTION`, collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis
* `-a/--authors NUMBER_OF_AUTHORS`, results with a given number of authors or less, e.g. 10
* `-r/--reversed`, sorts the items in chronological order

Default values are `E.Franzin.1` for the BAI, `article` for the collection and all the corresponding items in the Inspirehep database are sorted from the most recent.
