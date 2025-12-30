import numpy as np

from .load_samples import load_sample

from multilayer.algorithms import bet_centrality

def test_group_bet_centrality():
    """Test group betweeness centrality with a sample matrix."""
    data = load_sample()
    name = list(data.keys())[-1]
    
    centrality = bet_centrality.group_bet_centrality(data, [0,1,2,5], data[name].shape[0])
    expected = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    assert np.allclose(centrality, expected)