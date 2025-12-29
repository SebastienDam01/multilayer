import numpy as np
import multinetx as mx
from utils import multilayer_g, muxviz_aggregate
import config

def group_eigenvector_centrality(data, list_of_single_layers, N):
    """
    Return a flat list with the muxviz_aggregate output for EC, given a data, and a list_of_single_layers.

    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst

    list_of_layers: a list of numbers corresponding to the Multilayer you want to create -
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    N : layer size

    Returns
    -------
    out: An aggregate list which is the mean of the values of the EC per node in each layer
    """
    "This list will save all the eigenvector centralities for all individuals in all layers."
    name = list(data.keys())[-1]
    # fixed it!!!
    if len(data[name].shape) == 2:
        number_of_individuals = 1
    else:
        number_of_individuals = data[name].shape[2]

    group_eigenvector = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)

        m = mx.eigenvector_centrality_numpy(temp)
        # m=mx.eigenvector_centrality(multilayer_g(individual,number_of_layers,list_of_layers))
        temp1 = list(m.values())
        temp2 = muxviz_aggregate(temp1, len(list_of_single_layers))
        # temp2=aggregate(temp1,len(list_of_single_layers))
        # This is a list of lists with all centralities for all individuals
        group_eigenvector.append(temp2)
        # since we want to build a flat list
    flat_list = [item for sublist in group_eigenvector for item in sublist]

    return flat_list

# The functions below calculate mean and standard deviation of the measures
    
def group_eigenvector_centrality_mean(data, list_of_single_layers, N):
    """
    Return a flat list with the aggregate output for group eigenvector centrality mean, given a data, and a list_of_single_layers.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', 
    '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    Returns
    -------
    out: An aggregate list which is the mean of the values of the eigenvector centralities per node in each layer
    """
    "This function returns the group eigenvector centrality mean for all individuals"
    name = list(data.keys())[-1]
    if len(data[name].shape)==2:
        number_of_individuals=1
    else:
        number_of_individuals = data[name].shape[2]

    group_eigenvector_mean = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)

        m = mx.eigenvector_centrality_numpy(temp)
        temp1 = list(m.values())
        temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
        # Now we just compute the mean
        group_eigenvector_mean.append(np.mean(temp2))
        
    return (group_eigenvector_mean)


def group_eigenvector_centrality_std(data, list_of_single_layers, N):
    """
    Return a flat list with the aggregate output for group eigenvector centrality standard deviation, given a data, and a list_of_single_layers.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', 
    '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]
    
    Returns
    -------
    out: An aggregate list which is the standard deviation of the eigenvector centralities per subject
    """
    "This function returns the group eigenvector centrality standard deviation for all individuals"
    
    name = list(data.keys())[-1]
    if len(data[name].shape)==2:
        number_of_individuals=1

    else:
        number_of_individuals = data[name].shape[2]
    group_eigenvector_std = []
    for individual in range(number_of_individuals):
        temp = multilayer_g(individual, data, list_of_single_layers, N)
        m = mx.eigenvector_centrality_numpy(temp)
        #m=mx.eigenvector_centrality(multilayer_g(individual,number_of_layers,list_of_layers))
        temp1 = list(m.values())
        temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
        # This is MV aggregate - we can change then later for something else if needed
        
        group_eigenvector_std.append(np.std(temp2))
        
    return (group_eigenvector_std)


def eigenvector_centrality(individual, data, list_of_single_layers):
    """
    Return a histogram with the values of the Eigenvector centrality for all nodes for a chosen individual.
    
    Parameters
    ----------
    individual: an integer from [0, S-1], where S is the size of the cohort.
        
    data : A preloaded .mat  - Ex: supra_mst
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]
    
    Returns
    -------
    out: A list with EC for one individual
    """
    print('layers =',[config.layer_tags[i] for i in list_of_single_layers])
    m = mx.eigenvector_centrality_numpy(multilayer_g(individual, data, list_of_single_layers))
    temp1 = list(m.values())
    temp2=muxviz_aggregate(temp1,len(list_of_single_layers))
   
    return temp2