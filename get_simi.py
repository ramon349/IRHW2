import os 
import pandas as pd 
import sys 
import pdb 
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
    uniqID=full_data['qid'].unique()
    for ID in uniqID:
        if ID == 11110.0:
          pdb.set_trace()
        print("Processing query: {} ".format(ID))
        #get the datasets with the same query id 
        data_subset=full_data.loc[full_data['qid']==ID].reset_index()
        simi_map_subset=simi_map.loc[simi_map['qid']==ID].reset_index()
        simi_feats_subset=simi_feats.loc[simi_feats['qid'] ==ID].reset_index()
        for i,e in data_subset.iterrows():
            sample_did=e['did']
            idx = simi_map_subset.loc[simi_map_subset['did']==sample_did].index[0]
            feat = simi_feats_subset['meanCol'][idx]
            data_list.append(feat)
    myStuff = pd.DataFrame.from_dict({'simi':data_list})
    full_data = pd.concat((full_data,myStuff),axis=1)
    return full_data
def consume_data(simiFile):
    with open(simiFile,'r') as f:
        counter =0 
        for e in f:
            yield parse_row(e)
            counter+=1
        print("reads we performed {}".format(counter))
def write_data(outputFile,data_list):
    with open(outputFile, 'w') as f:
        counter =0 
        for e in data_list:
            f.write("{} {} {}".format(e[0],e[1],e[2]))
            f.write('\n')
            counter+=1
        print("writes we performed {}".format(counter))
if __name__ == "__main__":
    data_list = list() 
    simiFile = sys.argv[1]
    outputFile = sys.argv[2]
    data = consume_data(simiFile)
    write_data(outputFile,data)
