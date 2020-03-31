import pandas as pd 
from glob import glob



if __name__ == "__main__":
    files = glob('*perf*.txt')
    for e in files: 
        data = pd.read_csv(e,sep='\t',)
        other=data.mean(axis=0).to_frame().transpose()
        other['fold']='avg'
        new_data=pd.concat((data,other),axis=0)
        new_data.to_csv(e,index=False,sep='\t')