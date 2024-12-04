# Select the collection
def select_collection(data, x):
    return data if x == 'all' else [hit for hit in data if x in hit['metadata']['document_type']]


# Select published (refereed) hits
def select_published(data):
    return [hit for hit in data if 'refereed' in hit['metadata']]


# Select the interval
def select_interval(data, range):
    return [hit for hit in data if hit['metadata']['publication_or_earliest_date'] in range]


# Select the hits with n authors or less
def select_lessauthors(data, n):
    return [hit for hit in data if hit['metadata']['author_count'] <= n]


# Get the year range of publications
def get_years_range(data):
    first_year = None
    last_year = None
    for hit in data:
        hit_date = hit['metadata']['publication_or_earliest_date']
        if first_year is None or hit_date < first_year:
            first_year = hit_date
        if last_year is None or hit_date > last_year:
            last_year = hit_date
    years_range = last_year - first_year + 1
    return first_year, last_year, years_range


# Return warnings if data is empty
def warnings(data, number_of_authors, latest_years, given_year, collection):
    warning_parts = []
    total_hits = len(data)
    sa_string = 'single-author ' if number_of_authors == 1 else ''
    if total_hits == 0:
        if latest_years or given_year:
            warning_parts.append('in the selected period')
        if number_of_authors > 1:
            warning_parts.append(f'with less than {number_of_authors} authors')
        if collection != 'all':
            warning_parts.append(f'in the \033[3m{collection}\033[0m collection')
        warning = f'No {sa_string}research work {", ".join(warning_parts)}.'
        return warning
    else:
        return None
