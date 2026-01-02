import os
import numpy as np
from scipy.io import loadmat, savemat

try:
    TEST_DIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    TEST_DIR = os.getcwd()
MAT_DIR = os.path.join(TEST_DIR, 'matrices')

NODE_NUMBER=15
    
def mat_path(fname):
    """
    Return the full path to a test file located in the tests/matrices directory.

    Parameters
    ----------
    fname : str
        The filename (or relative path) of the test file.

    Returns
    -------
    str
        The absolute path by joining the test directory and the filename.
    """
    return os.path.join(MAT_DIR, fname)
    
def save_sample():
    """Save the sub-graph of dimensions NODE_NUMBERxNODE_NUMBER of the first individual of `supra_randmst.mat` in the test folder."""
    data = loadmat("supra_randmst.mat")
    name = list(data.keys())[-1]
    sample = data[name][:NODE_NUMBER, :NODE_NUMBER, 0]
    savemat(mat_path("sample_data.mat"), {
        "sample": sample
    })
    return

def save_full_sample():
    """Save the entire graph of the first individual of `supra_randmst.mat` in the test folder."""
    data = loadmat("supra_randmst.mat")
    name = list(data.keys())[-1]
    sample = data[name][..., 0]
    savemat(mat_path("full_sample_data.mat"), {
        "sample": sample
    })
    return

def load_sample():
    """Load a truncated sample data from a test file located in the test directory."""
    return loadmat(mat_path("sample_data.mat"))

def load_full_sample():
    """Load a full sample data from a test file located in the test directory."""
    return loadmat(mat_path("full_sample_data.mat"))

def save_chain_graph(n=NODE_NUMBER):
    """
    Save an undirected chain graph with n nodes to a .mat file.
    
    Parameter
    ---------
    n: Number of nodes
    """
    A = np.zeros((n, n), dtype=int)
    
    for i in range(n - 1):
        A[i, i + 1] = 1
        A[i + 1, i] = 1
    
    savemat(mat_path("chain_graph.mat"), {"chain_graph": A})
    return 

def load_chain_graph(n=NODE_NUMBER):
    """Load a chain graph from a test file located in the test directory."""
    return loadmat(mat_path("chain_graph.mat"))

