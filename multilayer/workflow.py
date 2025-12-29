import sys

import scipy

import utils, viz, config
from algorithms import bet_centrality, clustering, degree_centrality, eccentricity, eigenvector_centrality

FUNCTIONS = {
    "group_eigenvector_centrality": eigenvector_centrality.group_eigenvector_centrality,
    # TO DO
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
    layers: list of desired layers.
    """
    temp = function(data, layers, N)
    #You should include the desired subnetwork here. Now we have the whole Network.
    sub_net = list(range(0,N)) 
    # Ex: If you want FPN, sub_net=[16,17,18,19,20,21,28,29,30,31,93,94,123,124,133,134,163,164]
    
    temp_sub_net = utils.mask_subnetwork(temp, sub_net, N)
    utils.save_csv(temp_sub_net, filename, colname)
    
    return

def _main(argv=None):
    from cli.run import _get_parser
    
    options = _get_parser().parse_args(argv)
    
    supra_mst = scipy.io.loadmat(options.filename)
    
    ########################
    #Monolayer EC - No Mask#
    ########################

    for i in range(0,8):
        filename='Random_No_Mask_Group_MST_Mono_layer_real_'+config.layer_dic[i]+'_tag_'+str(i)
        colname='Random_No_Mask_Group_MST_Mono_layer_real_'+config.layer_dic[i]+'_tag_'+str(i)
        print(filename)
        print(colname)
        Data=supra_mst
        multilayer(FUNCTIONS[options.function], Data, filename, colname, [i], options.layer_size)

if __name__ == "__main__":
    _main()