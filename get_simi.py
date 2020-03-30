import os 
import pandas as pd 
import sys 

def load_similarity_features():
    data_feats= pd.read_csv('./simi_features.txt',names=['qid','qdid','meanCol'],sep=" ")
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

def add_simi(full_data:pd.DataFrame,simi_feats,simi_map):
    data_list = list() 
    for i,e in full_data.iterrows():
        sample_qid  = int(e['qid'])
        sample_did = e['did']
        matches= simi_map.loc[simi_map['did']==sample_did] #find document match
        idx= matches.loc[matches['qid'] ==sample_qid].index[0]
        feat=simi_feats.iloc[idx]['meanCol']
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
