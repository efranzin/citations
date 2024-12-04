def compute_metrics(cits, cits_noself, years_range):
    import numpy as np

    # Return None if the array is empty
    if len(cits) == 0:
        return None

    # Convert lists to numpy arrays
    cits_array = np.array(cits)
    cits_noself_array = np.array(cits_noself)

    # Number of hits
    total_hits = len(cits_array)

    # Save arrays [1,2,3,...] and [1,4,9,...]
    hits_array = np.arange(1, total_hits + 1)
    hits_array_squared = np.square(hits_array)

    # Sort the citation arrays in decreasing order
    cits_array_sorted = np.sort(cits_array)[::-1]
    cits_noself_array_sorted = np.sort(cits_noself_array)[::-1]

    # h-index: number of articles with at least h citations
    h_index = np.max(np.minimum(cits_array_sorted, hits_array))
    h_index_noself = np.max(np.minimum(cits_noself_array_sorted, hits_array))

    # i10-index: number of articles with at least 10 citations
    i10_index = (cits_array >= 10).sum()
    i10_index_noself = (cits_noself_array >= 10).sum()

    # g-index: largest number of top g articles, which have received together at least g^2 citations
    g2_index = np.max(np.minimum(np.cumsum(cits_array_sorted), hits_array_squared))
    g_index = int(np.sqrt(g2_index))
    g2_index_noself = np.max(np.minimum(np.cumsum(cits_noself_array_sorted), hits_array_squared))
    g_index_noself = int(np.sqrt(g2_index_noself))

    # m-index: h-index divided by the number of active years
    m_index = h_index / years_range
    m_index_noself = h_index_noself / years_range

    # Return the indices as a dictionary
    return {'h-index': h_index,
        'h-index_noself': h_index_noself,
        'i10-index': i10_index,
        'i10-index_noself': i10_index_noself,
        'g-index': g_index,
        'g-index_noself': g_index_noself,
        'm-index': m_index,
        'm-index_noself': m_index_noself}
