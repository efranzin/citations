import numpy as np

# Count the number of hits in each collection
def count_document_type(data):
    doc_type_counts = {}
    for hit in data:
        doc_type = hit['metadata']['document_type']
        for doc in doc_type:
            if doc in doc_type_counts:
                doc_type_counts[doc] += 1
            else:
                doc_type_counts[doc] = 1
    return doc_type_counts


# Count the number of hits per year
def count_documents_per_year(data):
    year_counts = {}
    for hit in data:
        hit_date = hit['metadata']['publication_or_earliest_date']
        if hit_date in year_counts:
            year_counts[hit_date] += 1
        else:
            year_counts[hit_date] = 1
    return year_counts


# Print the total number of citations (for all, citeable and published hits)
def print_totals(total, label=None):
    if label:
        print(f"Total number of citations: {total['total']}; Excluding self cites: {total['noself']} {label}")
    else:
        print(f"Total number of citations: {total['total']}; Excluding self cites: {total['noself']}")


# Categories and bin edges
bin_edges = np.array([1,10,50,100,250,500])
categories = ['unknown (0)',
    'less known (1–9)',
    'known (10–49)',
    'well-known (50–99)',
    'very well-known (100–249)',
    'famous (250–499)',
    'renowned (500+)']


# Function to get histogram data
def get_histogram(citations):
    bin_indices = np.digitize(citations, bin_edges)
    return list(np.bincount(bin_indices, minlength=7))


# Compute and print the breakdown of papers
def breakdown_citations(cits_citeable, cits_noself_citeable, cits_published, cits_noself_published):
    total_hits_citeable = len(cits_citeable)
    total_hits_published = len(cits_published)

    if total_hits_citeable <= 1:
        return None

    # Generate histograms for different citation arrays
    hist_citeable = get_histogram(cits_citeable)
    hist_citeable_noself = get_histogram(cits_noself_citeable)
    if total_hits_published > 0:
        hist_published = get_histogram(cits_published)
        hist_published_noself = get_histogram(cits_noself_published)

    hists = [('citeable', hist_citeable), ('citeable-noself', hist_citeable_noself)]
    if total_hits_published > 0:
        hists += [('published', hist_published), ('published-noself', hist_published_noself)]

    breakdown = {j: {category: hist[i] for i, category in enumerate(categories)} for j, hist in hists}

    output = f'\n--Breakdown of papers by citations--'
    output += f'\n{"":<26} {"Citeable":^9}'
    if total_hits_published != 0:
        output += f' {"Published":^9}'
    for category in categories:
        output += f'\n{category:<26} {breakdown["citeable"][category]:>4}|{breakdown["citeable-noself"][category]:<4}'
        if total_hits_published != 0:
            output += f' {breakdown["published"][category]:>4}|{breakdown["published-noself"][category]:<4}'
    return output
