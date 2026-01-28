# Parse options
import argparse
import configparser

# Load default values from config.ini
config = configparser.ConfigParser()
config.optionxform = str # config.ini case-sensitive
config.read('config.ini')
default_BAI = config['DEFAULT'].get('BAI', 'default')
default_collection = config['DEFAULT'].get('collection', 'article')

parser = argparse.ArgumentParser(description='Given an author identified by his/her BAI, this simple Python3 script counts the number of citations and the number of citations excluding self cites in the Inspirehep database (https://inspirehep.net/) for each paper in a given collection.')
parser.add_argument('-b', '--BAI', dest='BAI',
                  help='BAI identifier', default=default_BAI)
# argument -y/--year is not allowed with argument -l/--latest, and vice versa
year_range_group = parser.add_mutually_exclusive_group()
year_range_group.add_argument('-y', '--year', dest='given_year', type=int,
                  help='results for a given year, e.g. 2020')
year_range_group.add_argument('-l', '--latest', dest='latest_years', type=int,
                  help='results for the latest given years, e.g. 5')
parser.add_argument('-c', '--collection', dest='collection',
                  help='collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis; default: article', default=default_collection)
parser.add_argument('-a', '--authors', dest='number_of_authors', type=int,
                  help='results with a given number of authors or less, e.g. 10')
parser.add_argument('-r', '--reversed', action='store_true', dest='order',
                  help='list the items in chronological order')

args = parser.parse_args()

if args.BAI == 'default':
    parser.error("No default BAI found in config.ini; please specify one using -b.")

collections = ['all', 'article', 'book', 'bookchapter', 'conferencepaper', 'introductory', 'lectures', 'note', 'proceedings', 'published', 'report', 'review', 'thesis']
if args.collection not in collections:
    parser.error(f"Collection not valid. Please select one among: {', '.join(collections)}.")

# Save BAI as default in config.ini if it was provided and is not already set
if default_BAI == 'default' and args.BAI != 'default':
    config['DEFAULT']['BAI'] = args.BAI
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(f"{args.BAI} saved as default BAI in config.ini.")
