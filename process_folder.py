import sys 
import os 
from glob import glob
#process folder

def get_row(fInterest,row,fold):
    interest =""
    with open(fInterest,'r') as f:
        for i,e in enumerate(f):
            if i == row:
                interest+= e.rstrip('\n') 
    interest_list = interest.split("\t")
    interest_list[0] = str(fold )
    return interest_list

def get_header(fInterest,row):
    interest =""
    with open(fInterest,'r') as f:
        for i,e in enumerate(f):
            if i == row:
                interest+= e.rstrip('\n') 
    interest_list = interest.split("\t")
    interest_list[0] = "fold"
    return interest_list



if __name__=="__main__":
    f2proc_path = sys.argv[1]
    f_interest = sys.argv[2]
    row = int(sys.argv[3])
    os.chdir(f2proc_path)
    proc_list = sorted(glob(f_interest))
    for i,e in enumerate(proc_list):
        if i ==0:
            items = get_header(e,row-1)
            print("\t".join(items))
        items=get_row(e,row,i+1)
        print("\t".join(items))