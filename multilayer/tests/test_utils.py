import numpy as np

from .load_samples import load_full_sample

from multilayer import utils

def test_prepare_multilayer():
    """Test prepare_multilayer with a sample matrix."""
    data = load_full_sample()
    name = list(data.keys())[-1]
    
    supra_randmst = data[name][..., np.newaxis]
    N=100
    layer_list = list(range(2))
    layers = utils.prepare_multilayer(data, layer_list, N)
    
    assert len(layers) == len(layer_list) # correct number of layers
    
    # Each extracted layer corresponds to the input supra-adjacency matrix diagonal blocks
    for i, layer_id in enumerate(layer_list):
        expected = supra_randmst[
            layer_id * N : (layer_id + 1) * N,
            layer_id * N : (layer_id + 1) * N,
            :
        ]

        assert layers[i].shape == expected.shape
        
def test_multilayer_g():
    """Test multilayer graph with a sample matrix."""
    data = load_full_sample()
    name = list(data.keys())[-1]
    
    supra_randmst = data[name][..., np.newaxis]
    N=100
    layer_list = list(range(2))
    mg = utils.multilayer_g(0, data, layer_list, N)
    
# supra_mst = scipy.io.loadmat("supra_randmst.mat")
# filename='EC_No_Mask_Group_MST_Multi_layer_random_'#+Layer_dic[i]+'_tag_'+str(i)
# colname='EC_No_Mask_Group_MST_Multi_layer_random_'#+Layer_dic[i]+'_tag_'+str(i)
# print(filename)
# print(colname)
# function=group_eigenvector_centrality
# Data=supra_mst
#%%
# multilayer(function,Data,filename,colname,list(range(8)), 197)
# print('we did it')
