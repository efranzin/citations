#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this simple Python3 script counts the
number of citations and the number of citations excluding self cites in the
Inspirehep database (https://inspirehep.net/) for each paper in a given collection.
"""

__author__ = 'Edgardo Franzin'
__version__ = '3.2'
__license__ = 'GPL'
__email__ = 'edgardo<dot>franzin<at>gmail<dot>com'


# Parser options
from parser import args

BAI = args.BAI
given_year = args.given_year
latest_years = args.latest_years
collection = args.collection
order = args.order
number_of_authors = args.number_of_authors

# Import datetime to set the current year
from datetime import datetime
current_year = datetime.today().year

# Import functions
from profile import load_profile
from selection import select_collection, select_interval, select_lessauthors, warnings, get_years_range

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
first_year, last_year, active_years = get_years_range(data)

# Sorting: default is from most recent
if order:
    data = data[::-1]

# Dataclass and arrays to compute the citation metrics for published papers
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Citations:
    cits: list = field(default_factory=list)
    cits_noself: list = field(default_factory=list)
    authors: list = field(default_factory=list)
    age: list = field(default_factory=list)

    def add_citations(self, cits_count, cits_noself_count, author_count, age_of_publication):
        self.cits.append(cits_count)
        self.cits_noself.append(cits_noself_count)
        self.authors.append(author_count)
        self.age.append(age_of_publication)

    # Convert internal lists to NumPy arrays
    def to_numpy(self, dtype=int):
        return {
            'cits': np.asarray(self.cits, dtype=dtype),
            'cits_noself': np.asarray(self.cits_noself, dtype=dtype),
            'authors': np.asarray(self.authors, dtype=dtype),
            'age': np.asarray(self.age, dtype=dtype),
        }

cits_total = Citations()
cits_citeable = Citations()
cits_published = Citations()

for hit in data:
    metadata = hit['metadata']
    cits_count = metadata['citation_count']
    cits_noself_count = metadata['citation_count_without_self_citations']
    author_count = metadata['author_count']
    age_of_publication = metadata['age_of_publication']

    cits_total.add_citations(cits_count, cits_noself_count, author_count, age_of_publication)

    if 'citeable' in metadata:
        cits_citeable.add_citations(cits_count, cits_noself_count, author_count, age_of_publication)

    if 'refereed' in metadata:
        cits_published.add_citations(cits_count, cits_noself_count, author_count, age_of_publication)

# Convert lists to NumPy arrays
cits_total = cits_total.to_numpy()
cits_citeable = cits_citeable.to_numpy()
cits_published = cits_published.to_numpy()

total_hits = cits_total['cits'].size
total_hits_citeable = cits_citeable['cits'].size
total_hits_published = cits_published['cits'].size

# Count the number of citations and citations excluding self cites
citations = {'total': {'total': np.sum(cits_total['cits']), 'noself': np.sum(cits_total['cits_noself'])},
    'published': {'total': np.sum(cits_published['cits']), 'noself': np.sum(cits_published['cits_noself'])},
    'citeable': {'total': np.sum(cits_citeable['cits']), 'noself': np.sum(cits_citeable['cits_noself'])}}

def bold(text):
    return f"\033[1m{text}\033[0m"

def italic(text):
    return f"\033[3m{text}\033[0m"

# For each record print the title, the number of citations and the number of citations excluding self cites
for i, hit in enumerate(data):
    title = hit['metadata']['titles'][0]['title']
    if 'refereed' in hit['metadata']:
        title += '*'
    print(f"{bold(title)}\
          \nNumber of citations: {cits_total['cits'][i]}; Excluding self cites: {cits_total['cits_noself'][i]}")

from summary import count_document_type, print_totals, breakdown_citations

# Number of research works
collection_title = collection if collection != 'all' else 'research works'
print(f'\nNumber of {italic(collection_title)}: {total_hits}, published*: {total_hits_published}, citeable: {total_hits_citeable}')
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
from metrics import compute_metrics
indices = compute_metrics(cits_published, active_years)
format_index = lambda idx: f'{idx:g}' if idx.is_integer() else f'{idx:.2f}'

if total_hits_published > 1:
    bibliometrics_last_years = f' (last {latest_years} years)' if latest_years else ''
    if given_year:
        print(f'\n--Bibliometrics{bibliometrics_last_years}--\nNumber of publications: {total_hits_published}, citeable: {total_hits_citeable}, year: {given_year}')
    else:
        print(f'\n--Bibliometrics{bibliometrics_last_years}--\nNumber of publications: {total_hits_published}, citeable: {total_hits_citeable}, active years: {active_years} ({first_year}–{last_year})')
    print(f"Mean number of citations per paper: {np.mean(cits_published['cits']):0.1f}; Excluding self cites: {np.mean(cits_published['cits_noself']):0.1f}")
    for index in indices:
        print(f'{index}: {format_index(indices[index][0])}; Excluding self cites: {format_index(indices[index][1])}')

# Breakdown of papers by citations
breakdown = breakdown_citations(cits_citeable['cits'], cits_citeable['cits_noself'], cits_published['cits'], cits_published['cits_noself'])
print(breakdown) if breakdown else None
