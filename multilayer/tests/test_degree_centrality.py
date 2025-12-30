import numpy as np

from .load_samples import load_sample

from multilayer.algorithms import degree_centrality

def test_group_degree_centrality():
    """Test group degree centrality with a sample matrix."""
    data = load_sample()
    name = list(data.keys())[-1]
    
    centrality = degree_centrality.group_degree_centrality(data, [0,1,2,5], data[name].shape[0])
    assert np.allclose(np.sum(centrality), 14.1538)
    
def test_group_degree_centrality_mean():
    """Test group degree centrality mean with a sample matrix."""
    data = load_sample()
    name = list(data.keys())[-1]
    
    centrality = degree_centrality.group_degree_centrality_mean(data, [0,1,2,5], data[name].shape[0])
    assert np.allclose(centrality[0], 0.943589)
    
def test_group_degree_centrality_std():
    """Test group degree centrality std with a sample matrix."""
    data = load_sample()
    name = list(data.keys())[-1]
    
    centrality = degree_centrality.group_degree_centrality_std(data, [0,1,2,5], data[name].shape[0])
    assert np.allclose(centrality[0], 0.0340166)