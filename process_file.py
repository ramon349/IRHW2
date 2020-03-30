import pandas as pd
import sys 
import os
from getSiteFeats import load_site_feats
from glob import glob
from shutil import rmtree
from get_simi import add_simi,load_similarity_features

def getFeatureNames():
    """  This is an arbitrary file i made containing "names" names for the original features
    """
    feat_names = list()
    with open('../utils/featureNames.txt', 'r') as f:
        for e in f:
            feat_names.append(e.rstrip('\n').lower().rstrip(' '))
    return feat_names


def load_site2id_map():
    """ loads a dictionary mapping from one id to another 
        maps from GTX-00-000 to corresponding numeric format 
        this is needed for attachign additional features
        TODO MAKE SURE THIS WORKS WITH THE 2008 VERSION
    """
    idmap = dict()
    with open('./utils/RefTable.txt', 'r') as f:
        for l in f:
            # print(f"The value is {l}")
            oid, nid = l.rstrip('\n').split('\t')
            idmap[nid] = int(oid)
    return idmap
def load_data(dataPath):
    """ This is meant to load the S1-S5.txt files 
    Basically loads the data as a pandas data frame using some preprocessing 
    to get numeric values out of it 
    """
    featNames = getFeatureNames()
    # This range corresponds with the useful features
    data = pd.read_csv(dataPath, names=featNames, sep=" ", usecols=range(0, 48))
    # this range corresponds with the ID column
    docIDS = pd.read_csv(dataPath, names=['did'], sep=" ", usecols=range(50, 51))
    inc = pd.read_csv(dataPath, names=['inc'], sep=" ", usecols=range(53, 54)) 
    prob = pd.read_csv(dataPath, names=['prob'], sep=" ", usecols=range(56, 57)) 

    # go through each column and make it actually numeric.  this is done by a series of consistent concats
    # i could change this to be a simple reasignment?
    for col_name in data.keys():
        # numeric_data = pd.concat((numeric_data,make_numeric(data[col_name],col_name) ),axis=1)
        data[col_name] = make_numeric(data[col_name], col_name)
    data = pd.concat((data, inc, prob, docIDS), axis=1)
    return (data, docIDS)


def make_numeric(data_col, name):
    """ Helper function to make a datacolumn numeric. 
    looks for string columns spliting away the : found in our features 
    """
    new_data = pd.DataFrame()
    data = list()
    if data_col.dtype == 'O':  # type o corresponds to python object. used for Strings
        for i, e in enumerate(data_col):
            data.append(float(e.split(':')[1]))  # Here split string and get the numerica data we care about
        return pd.DataFrame.from_dict({name: data})  # make a dict in place because why not
    else:
        return data_col


def build_output_stirng(data_row):
    """ Make a single data row into the proper string format 
    d qid:0000 1:feat_val .... 
    note here we are removing the # id= and inc= and prob= those are not used by the classifier 
    """
    output = "{} qid:{}".format(data_row[0],int(data_row[1]))
    features = ['tfbody', 'tfanchor', 'tftitle', 'tfurl',
                'tfdocument', 'idfbody', 'idfanchor', 'idftitle', 'idfurl',
                'idfdocument', 'tf*idfbody', 'tf*idfanchor', 'tf*idftitle', 'tf*idfurl',
                'tf*idfwholedocument', 'dlbody', 'dlanchor', 'dltitle', 'dlurl',
                'dlwholedocument', 'bm25body', 'bm25anchor', 'bm25title', 'bme25url',
                'bm25wholedocument', 'lmir.absofbody', 'lmir.absofanchor',
                'lmir.absoftitle', 'lmir.absofurl', 'lmir.absofwholedocument',
                'lmir.dirofbody', 'lmir.dirofanchor', 'lmir.diroftitle',
                'lmir.dirofurl', 'lmir.dirofwholedocument', 'lmir.jmofbody',
                'lmir.jmofanchor', 'lmir.jmoftitle', 'lmir.jmofurl',
                'lmir.jmofwholedocument', 'pagerank', 'inlinknumber', 'outlinknumber',
                'numberofslashinurl', 'lengthofurl', 'numberofchildpage',
                'multtfbodydlbody', 'linkinter', 'combi', 'powPageRank', 'meanTF', 'meanIDF', 'meanDL']
    for i, name in enumerate(features):
        output += " {}:{}".format(i+1,data_row[name])
    output += " #dodcid = {} inc = {} prob = {}".format(data_row['did'],int(data_row['inc']),data_row['prob'])

    return output


def write_data(data: pd.DataFrame, fname):
    """ Get the rows  convert them   to stirng one by one 
    """
    with open(fname, 'w') as f:
        for i, e in data.iterrows():
            stuff = build_output_stirng(e)
            f.write(stuff)
            f.write('\n')


def expand_data(filePath, idmap,simi_feats=None,simi_map=None):
    example = filePath  # "./MQ2007/S1.txt"
    data, docID = load_data(example)
    newID = list()
    for e in docID['did']:
        newID.append(idmap[e])
    # indexFrame = pd.DataFrame.from_dict({'id': newID})
    # data = pd.concat((data, indexFrame), axis=1)
    # data.set_index('id')
    #data = add_simi(data,simi_feats,simi_map)#add similarity features 
    data['multtfbodydlbody'] = data['tfbody'] * data['dlbody']
    data['linkinter'] = data['inlinknumber'] * data['outlinknumber']
    data['combi'] = data['tfdocument'] * data['idfdocument']
    data['powPageRank'] = data['pagerank'] * data['pagerank']
    data['meanTF'] = (data['tfbody'] + data['tfanchor'] + data['tftitle'] + data['tfurl'] + data['tfdocument']) / 5
    data['meanIDF'] = (data['idfbody'] + data['idfanchor'] + data['idftitle'] +
                       data['idfurl'] + data['idfdocument']) / 5
    data['meanDL'] = (data['dlbody'] + data['dlanchor'] + data['dltitle'] + data['dlurl'] + data['dlwholedocument']) / 5
    return data


def writeFold(output_dir, dataList):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    os.chdir(output_dir)
    concatData = pd.concat(dataList[0:3], axis=0)
    write_data(concatData, 'train.txt')
    write_data(dataList[3], 'vali.txt')
    write_data(dataList[4], 'test.txt')


if __name__ == "__main__":
    # load it in main instead of funciton because it's expensive to load
    print("Loading reference table")
    idmap = load_site2id_map()
    print("Done ")
    data_dir = sys.argv[1] #'./MQ2008/'  # this is the data directory
    # directory where data will be saved
    output_dir = sys.argv[2]#"./2008_augData1/"
    print("Will extract features for {} and save to {}".format(data_dir,output_dir))
    main_path = os.getcwd()
    os.chdir(data_dir)
    dataFiles = sorted(glob('S*'))  # here we get the files meant to be for training testing
    dataList = list()
#    (simi_feats,simi_map)= load_similarity_features()
    simi_feats,simi_map = None,None 
    for e in dataFiles:
        print("Loading and expanding {}".format(e))
        data = expand_data(e, idmap,simi_feats,simi_map)
        dataList.append(data)
        print("Done expanding {}".format(e))
    os.chdir(main_path)
    folds = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 0], [2, 3, 4, 0, 1], [3, 4, 0, 1, 2], [4, 0, 1, 2, 3]]
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    os.mkdir(output_dir)
    os.chdir(output_dir)
    for i, e in enumerate(folds):
        print("Saving fold {}".format(i))
        permutation = [dataList[idx] for idx in e]
        writeFold('Fold_{}'.format(i+1), permutation)
        os.chdir('../')
