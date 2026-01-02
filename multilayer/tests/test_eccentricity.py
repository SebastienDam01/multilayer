import numpy as np

from .load_samples import load_chain_graph

from multilayer.algorithms import eccentricity

def test_group_eccentricity():
    """Test group eccentricity with a sample matrix."""
    data = load_chain_graph()
    name = list(data.keys())[-1]
    
    eccentri = eccentricity.group_eccentricity(data, [0,1,2,5], data[name].shape[0])
    assert np.allclose(np.sum(eccentri), 11.888888)
    
def test_non_norm_group_eccentricity():
    """Test group eccentricity without normalization with a sample matrix."""
    data = load_chain_graph()
    name = list(data.keys())[-1]
    
    eccentri = eccentricity.non_norm_group_eccentricity(data, [0,1,2,5], data[name].shape[0])
    assert np.allclose(np.sum(eccentri), 749)