import os
from scipy.io import loadmat, savemat

try:
    TEST_DIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    TEST_DIR = os.getcwd()
    
def test_path(fname):
    """
    Return the full path to a test file located in the test directory.

    Parameters
    ----------
    fname : str
        The filename (or relative path) of the test file.

    Returns
    -------
    str
        The absolute path by joining the test directory and the filename.
    """
    return os.path.join(TEST_DIR, fname)
    
def save_sample():
    """Save the sub-graph of dimensions 15x15 of the first individual of `supra_randmst.mat` in the test folder."""
    data = loadmat("supra_randmst.mat")
    name = list(data.keys())[-1]
    sample = data[name][:15, :15, 0]
    savemat(test_path("sample_data.mat"), {
        "sample": sample
    })
    return

def load_sample():
    """Load a sample data from a test file located in the test directory."""
    return loadmat(test_path("sample_data.mat"))

