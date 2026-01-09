import sys

import scipy

from . import utils, config#, viz

import os

# Add the path to MuxVizPy/src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MuxVizPy', 'src')))
# sys.path.insert(0, os.path.abspath(os.path.join('..', 'MuxVizPy', 'src')))

from MuxVizPy import build, topology, versatility, plotMux

FUNCTIONS = {
    "connected_components": topology.get_connected_components,
    "path_statistics": topology.get_multi_path_statistics,
    "SP_similarity": topology.get_SP_similarity_matrix,
    "degree_centrality": versatility.get_multi_degree,
    "eigenvector_centrality": versatility.get_multi_eigenvector_centrality,
    "katz_centrality": versatility.get_multi_katz_centrality,
    "RW_centrality": versatility.get_multi_RW_centrality, # not working
    "hub_centrality": versatility.get_multi_hub_centrality,
    "auth_centrality": versatility.get_multi_auth_centrality,
    "Kcore_centrality": versatility.get_multi_Kcore_centrality,
}

# ATTENTION: THIS IS THE ONLY FUNCTION THAT THE USER NEEDS TO CALCULATE ANY MULTILAYER
# NETWORK MEASURE
### IMPROVEMENT: create a boolean that does stuff when a mask is chosen or not
def multilayer(function, data, filename, colname, layers, N):
    """
    Return the desired output for the MumoBrain database, or any other database organized similarly.
    
    THIS IS PROBABLY THE MOST IMPORTANT FUNCTION FOR THE USER OF THIS CODE, SINCE EVERYTHING WAS BUILT TO REACH THIS STAGE HERE
    
    Parameters
    ----------
    function: One of the functions developed in this code for Multilayer Networks
    data: The data we want to use: e.g., supra_mst
    filename: The name of the file you want to save
    colname: the name of the column tag in your file
    layers: number of layers # list of desired layers.
    """
    temp = function(data, layers, N)
    #You should include the desired subnetwork here. Now we have the whole Network.
    sub_net = list(range(0,N)) 
    # Ex: If you want FPN, sub_net=[16,17,18,19,20,21,28,29,30,31,93,94,123,124,133,134,163,164]
    
    # temp_sub_net = utils.mask_subnetwork(temp, sub_net, N)
    # utils.save_csv(temp_sub_net, filename, colname)
    
    return temp

def main(argv=None):
    from .cli.run import _get_parser
    import graph_tool.draw as gtdraw
    
    options = _get_parser().parse_args(argv)
    
    # class Options():
    #     pass
    # options = Options()
    # options.filename = 'supra_randmst.mat'
    # options.layer_size = 210
    # options.function = 'get_multi_eigenvector_centrality'
    
    data = scipy.io.loadmat(options.filename)
    # Get the array for MuxVizPy
    name = list(data.keys())[-1]
    supra_mst = data[name]
    
    filename='EC_No_Mask_MST_Multi_layer_real'
    colname='EC_No_Mask_MST_Multi_layer_real'
    print(filename)
    print(colname)
    print("mask_subnetwork temporarily disabled...")
    Data=supra_mst[..., 0] # Only one subject for the moment
    
    result = multilayer(FUNCTIONS[options.function], Data, filename, colname, options.layer_number, options.layer_size)
    
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

    print("Results:", result)

if __name__ == "__main__":
    main()