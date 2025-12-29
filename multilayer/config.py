# from algorithms import bet_centrality, clustering, degree_centrality, eccentricity, eigenvector_centrality

# FUNCTIONS = {
#     "group_eigenvector_centrality": eigenvector_centrality.group_eigenvector_centrality,
#     # TO DO
# }

# THE VARIABLES DEFINED BELOW NEED TO BE MODIFIED TO CORRESPOND WITH THE DATA OF THE USER.
# Please see the comments in this code as well as the readme on Github for instructions on how
# to use this code. Note that comments with more than one # should be ignored - they are for further developments.

""" The user should define the input file (supra-adjacency matrix) in the beginning of the code. 
The code is quite robust - as long as the matrices are created using a pipeline similar to the one in the Lab."""

# ####################
# # SETTINGS         #
# ####################

# # Sebastien DAM 20252912: These should probably go to an argument parser.

# layer_size = 197   # Define the number of nodes per layer. We used the BNA, with some regions removed
# weighted = False # We are now using MST matrices. Matrices are thus not weighted - if weighted, change to True

# # Specify the the supra adjacency matrices here
# # TRAINING RANDOM MATRIX
# filename = 'supra_randmst.mat'

# #########################################
# # CREATING LAYER TAGS                   #
# #########################################

# # Associating tags for each layer will be helpful for our coding. We used the ones below
# # These are the tags for the Multilayer Networks - It should match with the layers in the supra-adjacency matrix
 
print('0 = fmri, 1 = pli delta, 2 = pli theta, 3 = pli alpha1, 4 = pli alpha2, 5 = pli beta, 6 = pli gamma, 7 = DWI .') 

### IMPROVEMENT! WE CAN INCLUDE A FUNCTION TO CHECK THE TAGS FROM OUR FILES 

layer_tags=['0 = fmri', '1 = pli delta', '2 = pli theta', '3 = pli alpha1', '4 = pli alpha2', '5 = pli beta', '6 = pli gamma', '7 = DWI']
just_tags=['fmri', 'pli_delta', 'pli_theta', 'pli_alpha1', 'pli_alpha2', 'pli_beta', 'pli_gamma', 'DWI'] 
plot_tags=['fMRI', 'PLI delta', 'PLI theta', 'PLI alpha1', 'PLI alpha2', 'PLI beta', 'PLI gamma', 'DWI'] 

layer_dic = {}
for i in range(0 , len(just_tags)):
    layer_dic[i] = just_tags[i]
print(layer_dic)