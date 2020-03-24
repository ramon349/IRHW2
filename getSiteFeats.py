import pandas as pd 
import numpy as np 


def load_site_feats():
    """ 
    make sure this works for the 2008 dataset. i.e make it folder specific 
    """
    coulumnNames = ['id','depth','urlLength','childPages','parentID']
    data:pd.DataFrame= pd.read_csv('../sitemap.txt',names=coulumnNames,sep='\t')
    data.set_index('id')
    return data 

