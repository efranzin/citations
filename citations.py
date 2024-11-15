#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this simple Python3 script counts the
number of citations and the number of citations excluding self cites in the
Inspirehep database (https://inspirehep.net/) for each paper in a given collection.
"""

__author__ = 'Edgardo Franzin'
__version__ = '2.9'
__license__ = 'GPL'
__email__ = 'edgardo<dot>franzin<at>gmail<dot>com'

# Parse options
import argparse

parser = argparse.ArgumentParser(description='Given an author identified by his/her BAI, this simple Python3 script counts the number of citations and the number of citations excluding self cites in the Inspirehep database (https://inspirehep.net/) for each paper in a given collection.')
parser.add_argument('-b', '--BAI', dest='BAI',
                  help='BAI identifier; default: E.Franzin.1', default='E.Franzin.1')
parser.add_argument('-y', '--year', dest='y', type=int,
                  help='results for a given year')
parser.add_argument('-l', '--latestyears', dest='latestyears', type=int,
                  help='results for the latest given years')
parser.add_argument('-c', '--collection', dest='collection',
                  help='collections: all, article, book, bookchapter, conferencepaper, introductory, lectures, note, proceedings, published, report, review, thesis; default: article', default='article')
parser.add_argument('--lessauthors', action='store_true', dest='less_than_10_authors',
                  help='limit the results to publications with 10 authors or less')
parser.add_argument('-r', '--reversed', action='store_true', dest='order',
                  help='list the items in chronological order')

args = parser.parse_args()
BAI = args.BAI
y = args.y
latestyears = args.latestyears
collection = args.collection
order = args.order
less_than_10_authors = args.less_than_10_authors

# Import datetime to set the current year
from datetime import datetime
current_year = datetime.today().year

# Import the modules to open and reading URLs and the JSON encoder
import requests

# Import numpy
import numpy as np

# Open the INSPIRE-HEP profile
inspirehep_profile = 'https://inspirehep.net/api/literature?q=a+' + BAI

# Select the collection
match collection:
    case 'published':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=published'
    case 'all':
        inspirehep_profile_collection = inspirehep_profile
    case 'article':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=article'
    case 'book':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=book'
    case 'bookchapter':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=book%20chapter'
    case 'conferencepaper':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=conference%20paper'
    case 'introductory':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=introductory'
    case 'lectures':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=lectures'
    case 'note':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=note'
    case 'proceedings':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=proceedings'
    case 'published':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=published'
    case 'report':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=report'
    case 'review':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=review'
    case 'thesis':
        inspirehep_profile_collection = inspirehep_profile + '&doc_type=thesis'

# Number of hits, and year of the earliest and latest hit
earliest_hit = requests.get(inspirehep_profile_collection + '&sort=leastrecent&size=1').json()['hits']['hits']
latest_hit = requests.get(inspirehep_profile_collection + '&sort=mostrecent&size=1').json()['hits']['hits']
earliest_hit_date = int(earliest_hit[0]['metadata']['earliest_date'][:4])
latest_hit_date = int(latest_hit[0]['metadata']['earliest_date'][:4])

# Load the data
# Split in pages to avoid 502-bad-gateway server error for large literature
de = latest_hit_date
de_diff = 2
data = []
while de > earliest_hit_date + de_diff:
    page = inspirehep_profile_collection[:40] + 'de>{}+and+de<={}+and+'.format(str(de-de_diff),str(de)) + inspirehep_profile_collection[40:] + '&sort=mostrecent&size=500'
    data += requests.get(page).json()['hits']['hits']
    de -= de_diff
page = inspirehep_profile_collection[:40] + 'de<={}+and+'.format(str(de)) + inspirehep_profile_collection[40:] + '&sort=mostrecent&size=500'
data += requests.get(page).json()['hits']['hits']
total_hits = len(data)
hits = range(total_hits)

# Select published (refereed) hits
data_published = []
for i in hits:
    if 'refereed' in data[i]['metadata']:
        data_published.append(data[i])
total_hits_published = len(data_published)
hits_published = range(total_hits_published)

# If data is empty, exit
if total_hits == 0:
    print('No research works in the selected collection')
    exit()

# Select the year or the latest N years, if requested
hits_latest_years = []
hits_published_latest_years = []
if latestyears is not None:
    range_years = range(current_year-latestyears+1, current_year+1)
elif y is not None:
    range_years = range(y, y+1)

if latestyears is not None or y is not None:
    for i in hits:
        data_earliest_date = data[i]['metadata']['earliest_date']
        earliest_date = int(data_earliest_date[:4])

        if 'publication_info' in data[i]['metadata'] and 'year' in data[i]['metadata']['publication_info'][0]:
            publication_date = data[i]['metadata']['publication_info'][0]['year']
        else:
            publication_date = earliest_date
        last_date = max(earliest_date,publication_date)
        if last_date in range_years:
            hits_latest_years.append(i)
    for i in hits_published:
        if 'year' in data_published[i]['metadata']['publication_info'][0]:
            data_published_date = data_published[i]['metadata']['publication_info'][0]['year']
            if data_published_date in range_years:
                hits_published_latest_years.append(i)

    hits = hits_latest_years
    hits_published = hits_published_latest_years
    total_hits = len(hits)
    total_hits_published = len(hits_published)

#If data is empty, exit
if total_hits == 0 and (latestyears or y is not None):
    print('No research works in the selected period')
    exit()

# Select the publications with 10 authors or less
authors_limit = 10
hits_less_than_10_authors = []
hits_published_less_than_10_authors = []
if less_than_10_authors == True:
    for i in hits:
        author_count = data[i]['metadata']['author_count']
        if author_count <= authors_limit:
            hits_less_than_10_authors.append(i)
    for i in hits_published:
        author_count = data_published[i]['metadata']['author_count']
        if author_count <= authors_limit:
            hits_published_less_than_10_authors.append(i)

    hits = hits_less_than_10_authors
    hits_published = hits_published_less_than_10_authors
    total_hits = len(hits)
    total_hits_published = len(hits_published)

# Year of the first and last entry
years_list = []
for i in hits:
    earliest_date = int(data[i]['metadata']['earliest_date'][:4])
    if 'publication_info' in data[i]['metadata'] and 'year' in data[i]['metadata']['publication_info'][0]:
        publication_date = data[i]['metadata']['publication_info'][0]['year']
    else:
        publication_date = earliest_date
    years_list.append(max(earliest_date,publication_date))
first_year = min(years_list)
last_year = max(years_list)

# Sorting: default is from most recent
if order == True:
    hits = reversed(hits)

# For each record print the title, the number of citations and the number of citations excluding self cites
totcits = totcits_noself = totcits_published = totcits_noself_published = totcits_citeable = totcits_noself_citeable = 0

# Arrays to compute the h-index for published papers
cits_array_published = cits_noself_array_published = np.empty(0,int)
cits_array_citeable = cits_noself_array_citeable = np.empty(0,int)
i10_index = i10_index_noself = 0

# Count the number of authors
author_count_array = []

# Print the number of citations and the number of citations excluding self cites for each entry
for i in hits:
    title = data[i]['metadata']['titles'][0]['title']
    cits = data[i]['metadata']['citation_count']
    cits_noself = data[i]['metadata']['citation_count_without_self_citations']
    author_count_array = np.append(author_count_array, data[i]['metadata']['author_count'])
    if 'refereed' in data[i]['metadata']:
        title += '*'
        totcits_published += cits
        totcits_noself_published += cits_noself
        cits_array_published = np.append(cits_array_published,cits)
        cits_noself_array_published = np.append(cits_noself_array_published, cits_noself)
        if cits >= 10:
            i10_index += 1
        if cits_noself >= 10:
            i10_index_noself += 1
    if 'citeable' in data[i]['metadata']:
        totcits_citeable += cits
        totcits_noself_citeable += cits_noself
        cits_array_citeable = np.append(cits_array_citeable, cits)
        cits_noself_array_citeable = np.append(cits_noself_array_citeable, cits_noself)
    print('\033[1m{}\033[0m'.format(title))
    print('Number of citations: {}; Excluding self cites: {}'.format(cits, cits_noself))
    totcits += cits
    totcits_noself += cits_noself

hits_array_published = np.arange(1, len(cits_array_published)+1)
hits_array_squared_published = np.square(hits_array_published)

total_hits_published = len(cits_array_published)
total_hits_citeable = len(cits_array_citeable)

# Compute some citation metrics https://en.wikipedia.org/wiki/Author-level_metrics
if len(cits_array_published) > 0:
    h_index = np.max(np.minimum(np.sort(cits_array_published)[::-1], hits_array_published))
    h_index_noself = np.max(np.minimum(np.sort(cits_noself_array_published)[::-1], hits_array_published))
    g2_index = np.max(np.minimum(np.cumsum(np.sort(cits_array_published)[::-1]), hits_array_squared_published))
    g_index = int(np.sqrt(g2_index))
    g2_index_noself = np.max(np.minimum(np.cumsum(np.sort(cits_noself_array_published)[::-1]), hits_array_squared_published))
    g_index_noself = int(np.sqrt(g2_index_noself))
    if y is not None:
        m_index = h_index
        m_index_noself = h_index_noself
    else:
        m_index = h_index/(last_year-first_year+1)
        m_index_noself = h_index_noself/(last_year-first_year+1)

collection_title = collection
if collection == 'all':
    collection_title = 'research works'
print('\nNumber of \033[3m{}\033[0m: {}, published*: {}, citeable: {}'.format(collection_title, total_hits, total_hits_published, total_hits_citeable))

# Print the total number of citations, the total number of citations excluding self cites, and the h-index
if total_hits > 0:
    print('Total number of citations: {}; Excluding self cites: {}'.format(totcits, totcits_noself))
if total_hits > 0 and total_hits != total_hits_citeable:
    print('Total number of citations: {}; Excluding self cites: {} (Citeable only)'.format(totcits_citeable, totcits_noself_citeable))
if total_hits_published > 0:
    print('Total number of citations: {}; Excluding self cites: {} (Published only)'.format(totcits_published, totcits_noself_published))
if len(cits_array_published) > 0:
    bibliometrics_last_years = ''
    if latestyears is not None:
        bibliometrics_last_years = ' (last ' + str(latestyears) + ' years)'
    if y is not None:
        print('\n--Bibliometrics{}--\nNumber of publications: {}, citeable: {}, year: {}'.format(bibliometrics_last_years, total_hits_published, total_hits_citeable, y))
    else:
        print('\n--Bibliometrics{}--\nNumber of publications: {}, citeable: {}, active years: {} ({}--{})'.format(bibliometrics_last_years, total_hits_published, total_hits_citeable, last_year-first_year+1, first_year, last_year))
    if less_than_10_authors is True:
        print('Max number of authors: {}'.format(authors_limit))
    # number of articles with at least h citations
    print('h-index: {}; Excluding self cites: {}'.format(h_index, h_index_noself))
    # number of articles with at least 10 citations
    print('i10-index: {}; Excluding self cites: {}'.format(i10_index, i10_index_noself))
    # largest number of top g articles, which have received together at least g^2 citations
    print('g-index: {}; Excluding self cites: {}'.format(g_index, g_index_noself))
    # h-index divided by the number of active years
    print('m-index: {:0.2f}; Excluding self cites: {:0.2f}'.format(m_index, m_index_noself))

# Breakdown of papers by citations
bin_edges = np.array([1,10,50,100,250,500])

bin_indices = np.digitize(cits_noself_array_published, bin_edges)
hist_published_noself = np.bincount(bin_indices, minlength=7)

bin_indices = np.digitize(cits_noself_array_citeable, bin_edges)
hist_citeable_noself = np.bincount(bin_indices, minlength=7)

bin_indices = np.digitize(cits_array_published, bin_edges)
hist_published = np.bincount(bin_indices, minlength=7)

bin_indices = np.digitize(cits_array_citeable, bin_edges)
hist_citeable = np.bincount(bin_indices, minlength=7)

categories = ('0', '1–9', '10–49', '50–99', '100–249', '250–499', '500+')
categories_title = ['unknown (0)', 'less known (1–9)', 'known (10–49)', 'well-known (50–99)', 'very well-known (100–249)', 'famous (250–499)', 'renowned (500+)']
if total_hits_published == 0:
    citations_c = {'Citeable': list(hist_citeable),
        'Citeable-noself': list(hist_citeable_noself)}
else:
    citations_c = {'Citeable': list(hist_citeable),
    'Citeable-noself': list(hist_citeable_noself),
    'Published': list(hist_published),
    'Published-noself': list(hist_published_noself)}

if total_hits > 1:
    print('\n--Breakdown of papers by citations--')
    if total_hits_published == 0:
        print('{:<26} {:5}'.format('', 'Citeable'))
    else:
        print('{:<26} {:5}\t {:5}'.format('', 'Citeable', 'Published'))
    for i in range(len(categories_title)):
        if total_hits_published == 0:
            print('{:<26} {:2}({})'.format(categories_title[i], citations_c['Citeable'][i], citations_c['Citeable-noself'][i]))
        else:
            print('{:<26} {:2}({})\t {:2}({})'.format(categories_title[i], citations_c['Citeable'][i], citations_c['Citeable-noself'][i], citations_c['Published'][i], citations_c['Published-noself'][i]))
