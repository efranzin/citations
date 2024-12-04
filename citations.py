#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this simple Python3 script counts the
number of citations and the number of citations excluding self cites in the
Inspirehep database (https://inspirehep.net/) for each paper in a given collection.
"""

__author__ = 'Edgardo Franzin'
__version__ = '3.0'
__license__ = 'GPL'
__email__ = 'edgardo<dot>franzin<at>gmail<dot>com'


# Parser options
from parser import *

# Import datetime to set the current year
from datetime import datetime
current_year = datetime.today().year

# Import functions
from profile import *
from selection import *

# Load and select data
data = load_profile(BAI)

if number_of_authors:
    data = select_lessauthors(data, number_of_authors)

data = select_collection(data, collection)

if latest_years:
    range_years = range(current_year-latest_years+1, current_year+1)
    data = select_interval(data, range_years)

if given_year:
    range_years = range(given_year, given_year+1)
    data = select_interval(data, range_years)

# Warning if data is empty
warning = warnings(data, number_of_authors, latest_years, given_year, collection)
if warning:
    print(warning)
    exit()

# Year of the first and last hits
first_year, last_year, years_range = get_years_range(data)

# Sorting: default is from most recent
if order == True:
    data = reversed(data)

# Lists to compute the citation metrics for published papers
cits_total = [hit['metadata']['citation_count'] for hit in data]
cits_noself_total = [hit['metadata']['citation_count_without_self_citations'] for hit in data]
cits_citeable = [hit['metadata']['citation_count'] for hit in data if 'citeable' in hit['metadata']]
cits_noself_citeable = [hit['metadata']['citation_count_without_self_citations'] for hit in data if 'citeable' in hit['metadata']]
cits_published = [hit['metadata']['citation_count'] for hit in data if 'refereed' in hit['metadata']]
cits_noself_published = [hit['metadata']['citation_count_without_self_citations'] for hit in data if 'refereed' in hit['metadata']]

total_hits = len(cits_total)
total_hits_citeable = len(cits_citeable)
total_hits_published = len(cits_published)

# Count the number of citations and citations excluding self cites
citations = {'total': {'total': sum(cits_total), 'noself': sum(cits_noself_total)},
    'published': {'total': sum(cits_published), 'noself': sum(cits_noself_published)},
    'citeable': {'total': sum(cits_citeable), 'noself': sum(cits_noself_citeable)}}

# For each record print the title, the number of citations and the number of citations excluding self cites
for i, hit in enumerate(data):
    title = hit['metadata']['titles'][0]['title']
    if 'refereed' in hit['metadata']:
        title += '*'
    print(f'\033[1m{title}\033[0m\
        \nNumber of citations: {cits_total[i]}; Excluding self cites: {cits_noself_total[i]}')

from summary import *

# Number of research works
collection_title = collection if collection != 'all' else 'research works'
print(f'\nNumber of \033[3m{collection_title}\033[0m: {total_hits}, published*: {total_hits_published}, citeable: {total_hits_citeable}')
if number_of_authors:
    print(f'Max number of authors: {number_of_authors}')
if collection == 'all':
    # Print the breakdown of document types by number; the sum of values can be larger that total_hits
    doc_type_counts = count_document_type(data)
    for key, value in sorted(doc_type_counts.items()):
        print(f'   {key}: {value}')

# Print the total number of citations with and without self cites
if total_hits > 1:
    print_totals(citations['total'])
if total_hits > 1 and total_hits != total_hits_citeable:
    print_totals(citations['citeable'], '(Citeable only)')
if total_hits_published > 1:
    print_totals(citations['published'], '(Published only)')

# Compute some citation metrics https://en.wikipedia.org/wiki/Author-level_metrics
# In this case they are computed for the published data
from metrics import *
indices = compute_metrics(cits_published, cits_noself_published, years_range)

if total_hits_published > 1:
    bibliometrics_last_years = f' (last {latest_years} years)' if latest_years else ''
    if given_year:
        print(f'\n--Bibliometrics{bibliometrics_last_years}--\nNumber of publications: {total_hits_published}, citeable: {total_hits_citeable}, year: {given_year}')
    else:
        print(f'\n--Bibliometrics{bibliometrics_last_years}--\nNumber of publications: {total_hits_published}, citeable: {total_hits_citeable}, active years: {years_range} ({first_year}–{last_year})')
    for index in ['h-index', 'i10-index', 'g-index', 'm-index']:
        if index == 'm-index':
            print(f"{index}: {indices[index]:0.2f}; Excluding self cites: {indices[f'{index}_noself']:0.2f}")
        else:
            print(f"{index}: {indices[index]}; Excluding self cites: {indices[f'{index}_noself']}")

# Breakdown of papers by citations
breakdown = breakdown_citations(cits_citeable, cits_noself_citeable, cits_published, cits_noself_published)
print(breakdown) if breakdown else None
