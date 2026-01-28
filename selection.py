# Select the collection
def select_collection(data, x):
    return data if x == 'all' else [hit for hit in data if x in hit['metadata'].get('document_type', [])]


# Select published (refereed) hits
def select_published(data):
    return [hit for hit in data if 'refereed' in hit['metadata']]


# Select the interval
def select_interval(data, range_years):
    return [hit for hit in data if hit['metadata']['publication_or_earliest_date'] in range_years]


# Select the hits with n authors or less
def select_lessauthors(data, n):
    return [hit for hit in data if hit['metadata']['author_count'] <= n]


# Get the year range of publications
def get_years_range(data):
    years = [hit['metadata']['publication_or_earliest_date'] for hit in data]
    first_year = min(years)
    last_year = max(years)
    active_years = last_year - first_year + 1
    return first_year, last_year, active_years

def italic(text):
    return f"\033[3m{text}\033[0m"

# Return warnings if data is empty
def warnings(data, number_of_authors, latest_years, given_year, collection):
    if data:
        return None

    warning_parts = []
    sa_string = 'single-author ' if number_of_authors == 1 else ''

    if latest_years or given_year:
        warning_parts.append('in the selected period')
    if number_of_authors is not None and number_of_authors > 1:
        warning_parts.append(f'with less than {number_of_authors} authors')
    if collection != 'all':
        warning_parts.append(f'in the {italic(collection)} collection')
    warning_text = f'No {sa_string}research work {", ".join(warning_parts)}.'
    return warning_text
