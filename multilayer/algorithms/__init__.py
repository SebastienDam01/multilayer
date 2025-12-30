"""
The network metric functions of `multilayer`.

They are organized into modules by types of metrics. 
One may find in a same module different functions to compute group or individual metrics. 

The strategy to create the functions is the same for every function; we can parse all NetworkX functions here.   
"""

from . import bet_centrality, clustering, degree_centrality, eccentricity, eigenvector_centrality
