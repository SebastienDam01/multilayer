import sys
import numpy as np
import pandas as pd
import scipy

from . import utils

import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MuxVizPy', 'src')))
# sys.path.insert(0, os.path.abspath(os.path.join('..', 'MuxVizPy', 'src')))

from MuxVizPy import build, mesoscale, topology, versatility, plotMux
import graph_tool as gt

FUNCTIONS = {
    "modularity": mesoscale.get_mod,
    "assortativity": mesoscale.inter_layer_assortativity,
    "clustering_coefficient": mesoscale.compute_local_clustering_coefficient_vector, # mesoscale.compute_local_clustering_coefficient,
    "connected_components": topology.get_connected_components,
    "path_statistics": topology.get_multi_path_statistics,
    "SP_similarity": topology.get_SP_similarity_matrix,
    "eccentricity": topology.get_eccentricity,
    "degree_centrality": versatility.get_multi_degree,
    "strength": versatility.compute_multi_strength_vector, # versatility.compute_multi_strength,
    "eigenvector_centrality": versatility.compute_eigenvector_centrality,
    "hub_centrality": versatility.get_multi_hub_centrality,
    "bridge_strength": versatility.get_bridge_strength,
}

# ATTENTION: THIS IS THE ONLY FUNCTION THAT THE USER NEEDS TO CALCULATE ANY MULTILAYER
# NETWORK MEASURE
### IMPROVEMENT: create a boolean that does stuff when a mask is chosen or not
def multilayer(function, data, filename, output_directory, colname, layers, N):
    """
    Return the desired output for the MumoBrain database, or any other database organized similarly.
    
    THIS IS PROBABLY THE MOST IMPORTANT FUNCTION FOR THE USER OF THIS CODE, SINCE EVERYTHING WAS BUILT TO REACH THIS STAGE HERE
    
    Parameters
    ----------
    function: One of the functions developed in this code for Multilayer Networks
    data: The data we want to use: e.g., supra_mst
    filename: The name of the file you want to save
    output_directory: The name of the directory you want to save
        Default: "results/"
    colname: the name of the column tag in your file
    layers: number of layers # list of desired layers.
    N: number of nodes per layer
    """
    # Build a table to identify all unique (=physical) nodes
    # node_table = pd.DataFrame({
    #     "layer":      [0] * N[0] + [1] * N[1],
    #     "local_node": list(range(N[0]))  + list(range(N[1])),
    #     "phys_node":  list(range(N[0]))  + list(range(N[0], N[0] + N[1])),  # disjoint example
    # })
    
    layer = []
    local_node = []
    phys_node = []
    
    # In the case where the first layer has its unique nodes and the other layers  have shared nodes (e.g., frequency bands), then the offset starts at the index corresponding to the number of nodes in the first layer
    shared_offset = N[0]
    
    for i, n in enumerate(N):
        layer.extend([i] * n)
        local_node.extend(range(n))
        if i == 0:
            # layer 0: unique nodes, not shared
            phys_node.extend(range(0, N[0]))
        else:
            # other layers: share the same nodes 
            phys_node.extend(range(shared_offset, shared_offset + n))
    
    node_table = pd.DataFrame({
        "layer": layer,
        "local_node": local_node,
        "phys_node": phys_node,
    })
    
    if function.__name__ == "get_mod": 
        adj = np.tril(data)
        idx = adj.nonzero()
        weights = adj[idx]
        g = gt.Graph(directed=False)
        g.add_edge_list(np.transpose(idx))
        
        #add weights as an edge propetyMap
        ew = g.new_edge_property("double")
        ew.a = weights 
        g.ep['weight'] = ew
        temp = list(function(g, layers))
    elif function.__name__ == "inter_layer_assortativity":
        g_list = build.supra_adjacency_to_network_list(data, layers, N)
        temp = function(g_list, layers)
    elif function.__name__ == "get_multi_path_statistics":
        temp = function(data, layers, N, node_table)
        if isinstance(temp, dict):
            for metric, value in temp.items():
                # FIXME implement subnetwork analysis
                basename, ext = filename.rsplit("_", maxsplit=1)
                new_filename = metric + "_" + ext
                utils.save_csv(value, new_filename, colname, output_directory)
            return temp
    elif function.__name__ == "compute_eigenvector_centrality" or \
    function.__name__ == "get_multi_hub_centrality" or \
    function.__name__ == "compute_local_clustering_coefficient" or \
    function.__name__ == "compute_multi_strength" or \
    function.__name__ == "compute_multi_strength_vector" or \
    function.__name__ == "compute_local_clustering_coefficient_vector" or \
    function.__name__ == "get_eccentricity":
        temp = function(data, layers, N, node_table)
    else:
        temp = list(function(data, layers, N))
        #You should include the desired subnetwork here. Now we have the whole Network.
        if isinstance(N, list):
            N = sum(N)
        sub_net = list(range(0,N))
        # Ex: If you want FPN, sub_net=[16,17,18,19,20,21,28,29,30,31,93,94,123,124,133,134,163,164]
        temp_sub_net = utils.mask_subnetwork(temp, sub_net, N)
        temp = temp_sub_net
        
    utils.save_csv(temp, filename, colname, output_directory)
    return temp

def main(argv=None):
    from .cli.run import _get_parser
    import graph_tool.draw as gtdraw
    
    options = _get_parser().parse_args(argv)
    
    if len(options.layer_size) == 1:
        options.layer_size = options.layer_size[0]
    
    print(f"Computing {options.function} for {options.filename} with {options.layer_number} layers and {options.layer_size} nodes:\n")
    
    data = scipy.io.loadmat(options.filename)
    # Get the array for MuxVizPy
    name = list(data.keys())[-1]
    supra_mst = data[name]
    
    filename=options.function + "_" + options.output_filename
    colname=options.function + "_" + options.output_filename
    print(filename)
    if len(supra_mst.shape)==2:
        Data=supra_mst
    else:
        Data=supra_mst[..., 0]
    
    result = multilayer(FUNCTIONS[options.function], Data, filename, options.output_directory, colname, options.layer_number, options.layer_size)
    
    if options.plotting:
        g_list = build.supra_adjacency_to_network_list(Data, options.layer_number, options.layer_size)
        
        # Aggregate graph for plotting
        g_agg = build.get_aggregate_network(g_list, obj_type="glist", return_mat=False)
        
        # Optional: fix layout for reproducibility
        positions = gtdraw.sfdp_layout(g_agg).get_2d_array([0, 1])
        
        plotMux.plotMultiplex(
        g_list,
        g_agg,
        positions=positions,     # uncomment if you computed positions above
        show_edges=True,           # intra-layer edges only
        size_mode="per_layer",        # same size scale across layers "global" or "per_layer"
        min_size=10.0,              # zero-degree nodes remain visible
        max_size=50.0,             # max bubble size
        max_edges_per_layer=8000,  # raise if layers are sparse & you want more lines
        edge_alpha=0.15,
        edge_lw=0.3,
        elev=20,
        azim=10,
        save_path="plots/myplot.png"
    )
    # print("Results: {}".format('\n '.join(map(str, result))))

if __name__ == "__main__":
    main()