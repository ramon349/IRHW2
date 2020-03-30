import os 
import pandas as pd 
import sys 

def load_similarity_features():
    data_feats= pd.read_csv('./simi_feats.txt',names=['qid','qdid','meanCol'],sep=" ")
    data_map = pd.read_csv('./simi_list.txt',names=['qid','did'],sep="\t")
    return (data_feats,data_map)

def parse_row(data_row):
    measurements = data_row.rstrip('\n').split(' ') 
    data_sum = 0.0
    for e in measurements[2:]:
        data_sum += float(e.split(':')[-1])
    data_sum /= (len(measurements) -2)
    queryid = measurements[0].split(":")[-1]
    qdid = measurements[1].split(':')[-1]
    return (queryid,qdid,data_sum)

def add_simi(full_data,simi_feats,simi_map):
    data_list = list() 
    for i,e in full_data.iterrows():
        sample_qid  = int(e['qid'])
        sample_did = e['did']
        #here we identify the query's  that exist and get a number of them
        query_matches = simi_map.loc[simi_map['qid']==sample_qid].reset_index()
        #from all the documetns belong to that query i now search for the matching 
        #document 
        idx = query_matches.loc[query_matches['did']==sample_did].index[0]
        #in the order of the queries with matchin qid this document is the idx element
        try:  
	    #i suspect the similarity features are incomplete... the ranking of documents
            #is incomplete. for some quuerys simi_feats only has 170 qid instead of a 1000
            feat=simi_feats.iloc[idx]['meanCol']
        except IndexError: 
            feat =0.0
        data_list.append(feat)
    myStuff = pd.DataFrame.from_dict({'simi':data_list})
    full_data = pd.concat((full_data,myStuff),axis=1)
    return full_data
if __name__ == "__main__":
    data_list = list() 
    simiFile = sys.argv[1]
    outputFile = sys.argv[2]
    with open(simiFile,'r') as f:
        for i,e in enumerate(f):
            data_list.append(parse_row(e))
    with open(outputFile, 'w') as f: 
        for e in data_list:
            f.write("{} {} {}".format(e[0],e[1],e[2]))
            f.write('\n')
