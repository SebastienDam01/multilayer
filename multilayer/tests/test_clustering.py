import numpy as np

from .load_samples import load_sample

from multilayer.algorithms import clustering

def test_group_clustering():
    """Test group clustering with a sample matrix."""
    data = load_sample()
    name = list(data.keys())[-1]
    
    cluster = clustering.group_clustering(data, [0,1,2,5], data[name].shape[0])
    expected_partial = np.array([0.875, 0.875, 1.0, 1.0])
    assert np.allclose(cluster[:4], expected_partial, atol=1e-6)
    assert np.allclose(np.sum(cluster), 14.5)
    assert len(cluster) == data[name].shape[0]