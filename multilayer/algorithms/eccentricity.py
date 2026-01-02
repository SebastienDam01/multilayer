import multinetx as mx
from multilayer.utils import multilayer_g, muxviz_aggregate

def group_eccentricity(data, list_of_single_layers, N):
    """
    Return a flat list with the aggregate output for group eccentricity, given a data, and a list_of_single_layers.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', 
    '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    Returns
    -------
    out: An aggregate list which is the mean of the values of the eccentricity per node in each layer
    """
    name = list(data.keys())[-1]
    if len(data[name].shape)==2:
        number_of_individuals=1
    else:
        number_of_individuals = data[name].shape[2]

    group_eccentricity = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)
        m = mx.eccentricity(temp)
        temp1 = list(m.values())
        temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
        # This is a list of lists with all eccentricities for all individuals
        group_eccentricity.append(temp2)
        # We want to buid a flat list 
    flat_list = [item for sublist in group_eccentricity for item in sublist]
        
    return flat_list


def non_norm_group_eccentricity(data, list_of_single_layers, N):
    """
    Return a flat list with the aggregate output for group eccentricity without normalization, given a data, and a list_of_single_layers.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', 
    '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    Returns
    -------
    out: An aggregate list which is the mean of the values of the eccentricity per node in each layer without normalization
    """
    name = list(data.keys())[-1]
    if len(data[name].shape)==2:
        number_of_individuals=1
    else:
        number_of_individuals = data[name].shape[2]

    group_eccentricity = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)

        m = mx.eccentricity(temp)
        temp1 = list(m.values())
        temp2 = temp1 
        # For non normalized, we don't apply the muxviz_aggregate function
        #muxviz_aggregate(temp1, len(list_of_single_layers)) 
        
        #temp2=aggregate(temp1,len(list_of_single_layers))
        # This is a list of lists with all eccentricities for all individuals
        group_eccentricity.append(temp2)
        # since we want to buid a flat list 
    flat_list = [item for sublist in group_eccentricity for item in sublist]
        
    return flat_list