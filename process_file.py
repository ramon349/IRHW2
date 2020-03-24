import pandas as pd 
from getSiteFeats import load_site_feats
from glob import glob 
from shutil import rmtree
import os 
def getFeatureNames():
    """  This is an arbitrary file i made containing "names" names for the original features
    """ 
    feat_names=  list()
    with open('./featureNames.txt','r') as f: 
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
    with open('./RefTable.txt','r') as f: 
        for l in f: 
            oid,nid= l.rstrip('\n').split('\t')
            idmap[nid]= int(oid)
    return idmap


def load_data(dataPath):
    """ This is meant to load the S1-S5.txt files 
    Basically loads the data as a pandas data frame using some preprocessing 
    to get numeric values out of it 
    """
    featNames = getFeatureNames() 
    #This range corresponds with the useful features
    data:pd.DataFrame = pd.read_csv(dataPath,names = featNames,sep=" ",usecols=range(0,48) ) 
    #this range corresponds with the ID column 
    docIDS = pd.read_csv(dataPath,names=['docid'],sep=" ",usecols=range(50,51))
    numeric_data = pd.DataFrame()
    #go through each column and make it actually numeric.  this is done by a series of consistent concats 
    #i could change this to be a simple reasignment? 
    for col_name in data.keys():
       # numeric_data = pd.concat((numeric_data,make_numeric(data[col_name],col_name) ),axis=1)
       data[col_name] = make_numeric(data[col_name],col_name)
    return (data,docIDS)
def make_numeric(data_col,name):
    """ Helper function to make a datacolumn numeric. 
    looks for string columns spliting away the : found in our features 
    """
    new_data= pd.DataFrame()
    data = list() 
    if data_col.dtype == 'O': #type o corresponds to python object. used for Strings 
        for i,e in enumerate(data_col):
            data.append(float(e.split(':')[1] ))#Here split string and get the numerica data we care about 
        return pd.DataFrame.from_dict({name:data}) #make a dict in place because why not
    else:
       return data_col
def build_output_stirng(data_row):
    """ Make a single data row into the proper string format 
    d qid:0000 1:feat_val .... 
    note here we are removing the # id= and inc= and prob= those are not used by the classifier 
    """
    output = f"{data_row[0]} qid:{data_row[1]}"
    for i in range(2,len(data_row)):
        output +=f" {i}:{data_row[i]}"
    return output 
def write_data(data: pd.DataFrame,fname):
    """ Get the rows  convert them   to stirng one by one 
    """
    with open(fname,'w') as f: 
        for i,e in data.iterrows():
            stuff = build_output_stirng(e)
            f.write(stuff)
            f.write('\n')
def expand_data(filePath,idmap):
    example =  filePath# "./MQ2007/S1.txt"
    data,docID = load_data(example)
    newID = list()
    for e in docID['docid']: 
        newID.append(idmap[e])
    indexFrame= pd.DataFrame.from_dict({'id':newID})
    data= pd.concat((data,indexFrame),axis=1)
    data.set_index('id')
    data['linkinter'] = data['inlinknumber']*data['outlinknumber']
    siteFeats = load_site_feats()
    data = pd.concat( [data,siteFeats] ,axis=1,join='inner' ).reindex(data.index) 
    return data
def writeFold(output_dir,dataList):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    os.chdir(output_dir)
    concatData = pd.concat(dataList[0:3],axis=0)
    write_data(concatData,'train.txt')
    write_data(dataList[3],'test.txt')
    write_data(dataList[4],'vali.txt')

if __name__ == "__main__": 
    #load it in main instead of funciton because it's expensive to load 
    idmap= load_site2id_map()
    data_dir= './MQ2007/'  #this is the data directory 
    #directory where data will be saved 
    output_dir = "./augData/"
    main_path = os.getcwd()
    os.chdir(data_dir)
    dataFiles= glob('S*') #here we get the files meant to be for training testing 
    dataList = list() 
    for e in dataFiles:
        data= expand_data(e,idmap)
        dataList.append(data) 
    os.chdir(main_path)
    folds =[  [0,1,2,3,4],[1,2,3,4,0],[2,3,4,0,1],[3,4,0,1,2],[4,0,1,2,3] ]
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    os.mkdir(output_dir)
    os.chdir(output_dir)
    for i,e in enumerate(folds):
        permutation = [dataList[idx] for idx in e]
        writeFold(f'Fold_{i}',permutation)
        os.chdir('../')
