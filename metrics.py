def compute_metrics(cits, years_range):
    import numpy as np

    # Return None if the array is empty
    if len(cits['cits']) == 0:
        return None

    # Convert lists to numpy arrays
    cits_array = np.array(cits['cits'])
    cits_by_author_array = np.array(cits['cits'])/np.array(cits['authors'])
    cits_noself_array = np.array(cits['cits_noself'])
    cits_noself_by_author_array = np.array(cits['cits_noself'])/np.array(cits['authors'])

    # Number of hits
    total_hits = len(cits_array)

    # Save arrays [1,2,3,...] and [1,4,9,...]
    hits_array = np.arange(1, total_hits + 1)
    hits_array_squared = np.square(hits_array)

    # Sort the citation arrays in decreasing order
    cits_array_sorted = np.sort(cits_array)[::-1]
    cits_noself_array_sorted = np.sort(cits_noself_array)[::-1]
    cits_by_author_array_sorted = np.sort(cits_by_author_array)[::-1]
    cits_noself_by_author_array_sorted = np.sort(cits_noself_by_author_array)[::-1]

    # h-index: number of articles with at least h citations
    h_index = np.max(np.minimum(cits_array_sorted, hits_array))
    h_index_noself = np.max(np.minimum(cits_noself_array_sorted, hits_array))

    # h-frac: fractional h-index
    h_frac = np.max(np.minimum(cits_by_author_array_sorted, hits_array))
    h_frac_noself = np.max(np.minimum(cits_noself_by_author_array_sorted, hits_array))

    # i10-index: number of articles with at least 10 citations
    i10_index = (cits_array >= 10).sum()
    i10_index_noself = (cits_noself_array >= 10).sum()

    # m-index: h-index divided by the number of active years
    m_index = h_index / years_range
    m_index_noself = h_index_noself / years_range

    # g-index: largest number of top g articles, which have received together at least g^2 citations
    g2_index = np.max(np.minimum(np.cumsum(cits_array_sorted), hits_array_squared))
    g_index = np.int64(np.sqrt(g2_index))
    g2_index_noself = np.max(np.minimum(np.cumsum(cits_noself_array_sorted), hits_array_squared))
    g_index_noself = np.int64(np.sqrt(g2_index_noself))

    # o-index: geometric mean of the h-index and the most cited paper
    o_index = np.sqrt(h_index * cits_array_sorted[0])
    o_index_noself = np.sqrt(h_index_noself * cits_noself_array_sorted[0])

    # L-index: combines citations, number of coauthors and age of publications
    L_index = np.log(1 + np.sum(np.array(cits['cits'])/(np.array(cits['authors'])*np.array(cits['age']))))
    L_index_noself = np.log(1 + np.sum(np.array(cits['cits_noself'])/(np.array(cits['authors'])*np.array(cits['age']))))

    # Return the indices as a dictionary
    return {'h-index': [h_index, h_index_noself],
        'h-frac': [h_frac, h_frac_noself],
        'i10-index': [i10_index, i10_index_noself],
        'm-index': [m_index, m_index_noself],
        'g-index': [g_index, g_index_noself],
        'o-index': [o_index, o_index_noself],
        'L-index': [L_index, L_index_noself]
        }
