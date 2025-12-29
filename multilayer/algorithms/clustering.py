import multinetx as mx
from utils import multilayer_g, muxviz_aggregate

def group_clustering(data, list_of_single_layers, N):
    """
    Return a flat list with the aggregate output for group clustering, given a data, and a list_of_single_layers.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', 
    '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    Returns
    -------
    out: An aggregate list which is the mean of the values of the Clustering per node in each layer
    """
    name = list(data.keys())[-1]
    if len(data[name].shape)==2:
        number_of_individuals=1
    else:
        number_of_individuals = data[name].shape[2]

    group_clustering = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)

        m = mx.clustering(temp)
        temp1 = list(m.values())
        temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
        # This is a list of lists with all centralities for all individuals
        group_clustering.append(temp2)
    # We want to buid a flat list 
    # Check this flattened = [val for sublist in list_of_lists for val in sublist]
    flat_list = [item for sublist in group_clustering for item in sublist]
        
    return flat_list