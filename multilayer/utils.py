from . import config
import numpy as np
import pandas as pd
import multinetx as mx

def prepare_multilayer(data, list_of_layers, N):
    """
    Convert the data to a Multinetx friendly object based on the inputed data.
    
    Parameters
    ----------
    data : A preloaded .mat  - Ex: supra_mst


    list_of_layers: a list of numbers corresponding to the Multilayer you want to create -
    Ex: If you want a Multilayer with fmri, pli_delta, pli theta, and pli beta using the tags: 0=fmri', '1=pli delta', '2= pli theta','5 = pli beta'
    list_of_layers = [0,1,2,5]

    Returns
    -------
    out : list of layers.
    Note: This is convenient - since we can have a database with all 14 layers, but we may want to study only a smaller number of layers.
    In short, the layers are based in the supra-adjacency matrices - but you can choose exactly the layers you want here"
    """
    # In the matlab file the element [-1] gives the matrices
    name = list(data.keys())[-1]
    if len(data[name].shape) == 2:
        multilayer = np.expand_dims(data[name], axis=0).T
    else:
        multilayer = data[name]

    # Just checking if there are NaNs
    where_are_NaNs = np.isnan(multilayer)
    multilayer[where_are_NaNs] = 0
    # layer_size = 197 # This are the numbers of nodes in the layer
    # N = layer_size
    layer_list = list_of_layers

    layers = []
    for i in layer_list:
        layers.append(multilayer[(i * N):(i + 1) * N, (i * N):(i + 1) * N, :])

    return layers


# This creates a multilayer network for each individual (This is the new one)
def multilayer_g(individual, data, list_of_single_layers, N):
    """
    Create a Multilayer graph object for an individual, given the data, and a list of layers.
    
    Parameters
    ----------
    Individual: an integer from [0, S-1], where S is the size of the cohort.

    data : A preloaded .mat  - Ex: supra_mst


    list_of_layers: a list of numbers corresponding to the Multilayer you want to create -
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]

    Returns
    -------
    out: A Multilayer Object for a single individual in the data.
    """
    "Creates a multilayer for an individual i, knowing the number of layers, and the size of the layers"
    layers = prepare_multilayer(data, list_of_single_layers, N)
    # N =197 # before was 205
    number_of_layers = len(list_of_single_layers)
    G = []
    for j in range(0, len(list_of_single_layers)):
        "j is running over all layers for a fixed individual i"
        G.append(mx.from_numpy_array(layers[j][:, :, individual]))

    # Define the type of interconnection between the layers

    # This creates the supra adjacency matrix
    adj_block = mx.lil_matrix(np.zeros((N * number_of_layers, N * number_of_layers)))  # N is the size of the layer

    # Need to create generic adjacency blocks!!!!

    # These are generic interconnection blocks!!!
    for i in range(number_of_layers):
        for j in range(number_of_layers):
            if i == j:
                adj_block[i * N:  (i + 1) * N, j * N:(j + 1) * N] = np.zeros(N)
            else:
                adj_block[i * N:  (i + 1) * N, j * N:(j + 1) * N] = np.identity(N)

    mg = mx.MultilayerGraph(list_of_layers=G, inter_adjacency_matrix=adj_block)
    mg.set_edges_weights(intra_layer_edges_weight=1, inter_layer_edges_weight=1)

    return mg


#############################
# CREATING THE AGGREGATE    #
#############################

# ATTENTION: THERE ARE SEVERAL OPTIONS HERE - WE ARE USING A SIMILAR AGGREGATION AS MUXVIZ (see http://muxviz.net/tutorial.php)
# THIS IS AN INTERMEDIATE FUNCTION SO THAT THE OUTPUT OF THE OTHER FUNCTIONS IS PRINTED 'PER NODE'
def muxviz_aggregate(multiple_layers_list, number_layers):
    """
    Create an aggregate output from a Multilayer Network, given a multiple_layers_list and the number of layers.
    
    Parameters
    ----------
    multiple_layers_list: output of a multilayer network metric

    number_layers: number of layers in the multilayer

    Returns
    -------
    out: An aggregate list which is the mean of the values of a Network property per node in each layer

    """
    k, m = divmod(len(multiple_layers_list), number_layers)
    temp = list(multiple_layers_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(number_layers))
    temp_mean = np.mean(temp, axis=0)
    temp_mean = temp_mean / max(temp_mean)
    # for sublists in temp:
    #    m=np.max(temp[sublists])
    #    for i in sublists:
    #        temp[sublists][i]=temp[sublists][i]/m

    return temp_mean

# This function extracts data from specific nodes - e.g. FPN or DMN
#### IMPROVEMENT: ALSO COMPUTE MEASURES WITHIN SPECIFIC SUBNETWORK IN THE FUTURE
def mask_subnetwork(result, target, N):
    """
    Return a multilayer metric narrowed for a given list of nodes, which for our purposes are subnetworks.
    
    Parameters
    ----------
    result: A list with the results (output) of any of Multilayer functions in this code
    
    target : A list of target nodes of interest, e.g., nodes from DFN or FPN
    
    N: The layer size
    
    Returns
    -------
    out: A list for the results narrowed for the target nodes, i.e., If you say the target nodes for a given subnetwork, this function returns only the results of the list associated with the target nodes"
    """
    chunks = [result[x:x+N] for x in range(0, len(result), N)]
    mask = [chunk[x] for chunk in chunks for x in target]
    
    return mask


# This function saves data to a csv file
def save_csv(data, name, tag):
    """
    Return a .csv file for further analysis using SPSS.
    
    Parameters
    ----------
    data: The desired data you want to save
    name: The name of the file you want to save
    tag: The tag for the variable/column in your .csv file
    """
    # Obs: Notice that if you want to get results only for a subnetwork, we should first do:
    #data=mask_subnetwork(result,target)
    #before saving this file
    cols = [tag]
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(name+'.csv')
    
    return