
# URL https://archive.ics.uci.edu/dataset/27/credit+approval 


#%%
# pip install --upgrade ipykernel

#%%
# pip install ucimlrepo
from ucimlrepo import fetch_ucirepo 

#%%
# fetch dataset 
credit_approval = fetch_ucirepo(id=27) 
  
#%%
# data (as pandas dataframes) 
X = credit_approval.data.features 
y = credit_approval.data.targets 

#%%  
# metadata 
print(credit_approval.metadata) 

#%%  
# variable information 
print(credit_approval.variables) 
