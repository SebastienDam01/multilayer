import matplotlib.pyplot as plt
import multinetx as mx
from . import config
from .utils import multilayer_g, muxviz_aggregate
from .algorithms.eigenvector_centrality import group_eigenvector_centrality

def plot_group_ec(data, list_of_single_layers):
    """
    Return a histogram plot with the values of the Eigenvalue centrality for all nodes across all individuals.
    
    Parameters
    ----------  
    data : A preloaded .mat  - Ex: supra_mst
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]
    
    Returns
    -------
    out : A histogram plot with EC for all nodes across all individuals
    """
    print('layers =',[config.layer_tags[i] for i in list_of_single_layers])

    temp = group_eigenvector_centrality(data,list_of_single_layers)
    plt.figure(figsize=(8,5))
    plt.hist(temp)
    # We can edit here the output if we have a vector with the name of the layers
    plt.xlabel('Eig. centr. - aggr- all nodes all individuals ', fontsize=20)
    #plt.xlim(-5,220)
    plt.ylabel("frequence", fontsize=20)
    #plt.xlim(40, 160)
    plt.ylim(0, 3500)
    #plt.title('individual '+str(individual))
    plt.show()


def plot_ec(individual, data, list_of_single_layers):
    """
    Return a histogram with the values of the Eigenvalue centrality for all nodes for a chosen individual.
    
    Parameters
    ----------
    individual: an integer from [0, S-1], where S is the size of the cohort.
        
    data : A preloaded .mat  - Ex: supra_mst
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]
    
    Returns
    -------
    out: A histogram with EC for one individual
    """
    print('layers =',[config.layer_tags[i] for i in list_of_single_layers])
    #multilayer_g(individual,data,list_of_single_layers)
    m = mx.eigenvector_centrality_numpy(multilayer_g(individual,data,list_of_single_layers))
    #temp=multlayer3(i)
    temp1 = list(m.values())
    temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
    # This is the Mux Viz aggregate - We change the aggregate here if yo want later
    plt.hist((temp2))
    ###IMPROVEMENT: We can edit here the output if we have a vector with the name of the layers
    plt.xlabel('Eigenvector centrality - aggregate ', fontsize=20)
    #We may also want to choose the range for the plot.
    #plt.xlim(min,max)
    plt.ylabel("frequence", fontsize=20)
    plt.ylim(0, 100)
    plt.title('individual '+ str(individual))
    plt.show()
    return