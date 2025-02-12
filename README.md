# `citations.py`

Before running the script you need to edit `config.ini` with your own BAI identifier, or specify it using `-b BAI`.
The first time you run the script it downloads the whole profile in a local .json file, it can take some minutes for very large bibliographies.
If the local database is at least one day old, it asks for updates. Otherwise you can run the script with the local data and it should be very fast.


## Usage

`citations.py [-b BAI] [-y GIVEN_YEAR | -l LATEST_YEARS] [-c COLLECTION] [-a NUMBER_OF_AUTHORS] [-r]`

### Options

* `-b/--BAI BAI`, specifies the author's BAI identifier
* `-y/--year GIVEN_YEAR`, results for a given year, e.g. 2020
* `-l/--latest LATEST_YEARS`, results for the latest given years, e.g. 5
* `-c/--collection COLLECTION`, collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis
* `-a/--authors NUMBER_OF_AUTHORS`, results with a given number of authors or less, e.g. 10
* `-r/--reversed`, sorts the items in chronological order

The default value for collection is `article`, and the items are sorted from the most recent.


## About the hit date

The function `get_hit_date(hit)` defined in [`profile.py`](profile.py#L8) for _published_ hits returns the maximum between the earliest date the hit appeared and the publication date; this is not the default behaviour of INSPIRE which always uses the earliest date.
