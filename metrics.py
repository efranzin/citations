import numpy as np

def compute_metrics(cits, active_years):
    # Return None if the array is empty
    if cits['cits'].size == 0:
        return None

    # Citations normalized by number of authors
    cits_by_author = cits['cits']/cits['authors']
    cits_noself_by_author = cits['cits_noself']/cits['authors']

    # Number of hits
    total_hits = cits['cits'].size

    # Save arrays [1,2,3,...] and [1,4,9,...]
    hits_array = np.arange(1, total_hits + 1)
    hits_array_squared = np.square(hits_array)

    # Sort the citation arrays in decreasing order
    cits_sorted = np.sort(cits['cits'])[::-1]
    cits_noself_sorted = np.sort(cits['cits_noself'])[::-1]
    cits_by_author_sorted = np.sort(cits_by_author)[::-1]
    cits_noself_by_author_sorted = np.sort(cits_noself_by_author)[::-1]

    # h-index: number of articles with at least h citations
    h_index = np.max(np.minimum(cits_sorted, hits_array))
    h_index_noself = np.max(np.minimum(cits_noself_sorted, hits_array))

    # h-frac: fractional h-index
    h_frac = np.max(np.minimum(cits_by_author_sorted, hits_array))
    h_frac_noself = np.max(np.minimum(cits_noself_by_author_sorted, hits_array))

    # i10-index: number of articles with at least 10 citations
    i10_index = (cits['cits'] >= 10).sum()
    i10_index_noself = (cits['cits_noself'] >= 10).sum()

    # m-index: h-index divided by the number of active years
    m_index = h_index / active_years
    m_index_noself = h_index_noself / active_years

    # g-index: largest number of top g articles, which have received together at least g^2 citations
    g2_index = np.max(np.minimum(np.cumsum(cits_sorted), hits_array_squared))
    g_index = np.int64(np.sqrt(g2_index))
    g2_index_noself = np.max(np.minimum(np.cumsum(cits_noself_sorted), hits_array_squared))
    g_index_noself = np.int64(np.sqrt(g2_index_noself))

    # o-index: geometric mean of the h-index and the most cited paper
    o_index = np.sqrt(h_index * cits_sorted[0])
    o_index_noself = np.sqrt(h_index_noself * cits_noself_sorted[0])

    # L-index: combines citations, number of coauthors and age of publications
    L_index = np.log(1 + np.sum(cits['cits']/(cits['authors'] * cits['age'])))
    L_index_noself = np.log(1 + np.sum(cits['cits_noself']/(cits['authors'] * cits['age'])))

    # Return the indices as a dictionary
    return {'h-index': [h_index, h_index_noself],
        'h-frac': [h_frac, h_frac_noself],
        'i10-index': [i10_index, i10_index_noself],
        'm-index': [m_index, m_index_noself],
        'g-index': [g_index, g_index_noself],
        'o-index': [o_index, o_index_noself],
        'L-index': [L_index, L_index_noself]
        }
