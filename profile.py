# Import datetime
from datetime import datetime
# Import the JSON encoder
import json


# Get the hit date
def get_hit_date(hit):
    earliest_date = int(hit['metadata']['earliest_date'][:4])
    publication_date = (hit['metadata'].get('publication_info', [{}])[0].get('year', earliest_date))
    # If available, use the year of publication
    return max(earliest_date, publication_date)
    # Notice that inspirehep.net uses 'earliest_date'


# Download the profile and save it locally
def download_profile(BAI):
    # Import the module to open and read URLs
    import requests
    # Import tqdm for the progress bar
    from tqdm import tqdm
    # Import sleep
    from time import sleep

    current_year = datetime.today().year

    # Open the INSPIRE-HEP profile
    inspirehep_profile = f'https://inspirehep.net/api/literature?q=a+{BAI}'

    try:
        response = requests.get(inspirehep_profile)
        response.raise_for_status()
        total_hits_profile = response.json()['hits']['total']

        # Check if empty
        if total_hits_profile == 0:
            print('Empty database. No data saved.')
            exit()

    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        exit()

    # Load the data; in pages to avoid 502-bad-gateway server error for large literature
    data = []
    page_number = 1
    page_size = 50
    pages = 1 + total_hits_profile // page_size

    with tqdm(total=pages, desc='Downloading data', unit='page') as pbar:
        while page_number <= pages:
            page = f'{inspirehep_profile}&sort=mostrecent&size={page_size}&page={page_number}'
            try:
                response = requests.get(page)
                response.raise_for_status()
                data += response.json()['hits']['hits']
                page_number += 1
                pbar.update(1)
                sleep(1)  # To avoid overwhelming the server
            except requests.exceptions.RequestException as e:
                print(f'Error fetching data: {e}')
                exit()

    # Strip the json to make a lighter file
    links_to_remove = ['bibtex', 'latex-eu', 'latex-us', 'json', 'cv']
    keys_to_remove = ['authors', 'references', 'abstracts', 'figures', 'referenced_authors_bais', '$schema', 'inspire_categories', 'public_notes', 'facet_author_name', 'license', 'copyright', 'documents', 'keywords']
    for hit in data:
        for link in links_to_remove:
            hit['links'].pop(link, None)
        for key in keys_to_remove:
            hit['metadata'].pop(key, None)
        doc_type = hit['metadata']['document_type']
        if 'publication_type' in hit['metadata']:
            doc_type += hit['metadata']['publication_type']
        doc_type = [doc.replace('conference paper', 'conferencepaper').replace('book chapter', 'bookchapter') for doc in doc_type]
        hit['metadata']['document_type'] = doc_type
        # Add the 'publication_or_earliest_date' key
        hit['metadata']['publication_or_earliest_date'] = get_hit_date(hit)
        # Add the 'age_of_publication' key
        hit['metadata']['age_of_publication'] = current_year - get_hit_date(hit) + 1

    # Save the profile
    filename = f'{BAI}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


# Ask for update if an older database is present
def prompt_update(datestamp):
    prompt_string = f'There is an old database with date {datestamp:%B %d, %Y}; do you want to update it? [y/n] '
    update = input(prompt_string).lower()
    while update not in ('y', 'n'):
        print('Please answer with y or n.')
        update = input(prompt_string).lower()
    return update == 'y'


# Load data from local file, check for updates, or download it
def load_profile(BAI):
    import os

    filename = f'{BAI}.json'
    current_date = datetime.today().date()

    # Check if a database is present
    if os.path.isfile(filename):
        # Check datestamp
        timestamp = os.path.getmtime(filename)
        datestamp = datetime.fromtimestamp(timestamp).date()
        # If the database has been downloaded today use it
        if datestamp == current_date:
            with open(filename, 'r') as file:
                data = json.load(file)
        # Otherwise ask for updates first, if answer is no use the current database
        else:
            if not prompt_update(datestamp):
                print('Database not updated.')
                with open(filename, 'r') as file:
                    data = json.load(file)
            else:
                data = download_profile(BAI)
    # Otherwise download it
    else:
        data = download_profile(BAI)

    return data
