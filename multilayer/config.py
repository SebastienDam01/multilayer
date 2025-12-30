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