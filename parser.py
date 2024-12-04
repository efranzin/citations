# Parse options
import argparse

parser = argparse.ArgumentParser(description='Given an author identified by his/her BAI, this simple Python3 script counts the number of citations and the number of citations excluding self cites in the Inspirehep database (https://inspirehep.net/) for each paper in a given collection.')
parser.add_argument('-b', '--BAI', dest='BAI',
                  help='BAI identifier; default: E.Franzin.1', default='E.Franzin.1')
# argument -y/--year is not allowed with argument -l/--latest, and vice versa
year_range_group = parser.add_mutually_exclusive_group()
year_range_group.add_argument('-y', '--year', dest='given_year', type=int,
                  help='results for a given year, e.g. 2020')
year_range_group.add_argument('-l', '--latest', dest='latest_years', type=int,
                  help='results for the latest given years, e.g. 5')
parser.add_argument('-c', '--collection', dest='collection',
                  help='collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis; default: article', default='article')
parser.add_argument('-a', '--authors', dest='number_of_authors', type=int, default=False,
                  help='results with a given number of authors or less, e.g. 10')
parser.add_argument('-r', '--reversed', action='store_true', dest='order',
                  help='list the items in chronological order')

args = parser.parse_args()
BAI = args.BAI
given_year = args.given_year
latest_years = args.latest_years
collection = args.collection
order = args.order
number_of_authors = args.number_of_authors

collections = ['all', 'article', 'book', 'bookchapter', 'conferencepaper', 'introductory', 'lectures', 'note', 'proceedings', 'published', 'report', 'review', 'thesis']
if args.collection not in collections:
    parser.error("Collection not valid. Please select one among: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis.")
