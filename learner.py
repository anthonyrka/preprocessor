import pandas as pd
import sys
import numpy as np
import statsmodels.api as sm
import json
import random

print '******BEGIN: LEARNING******'

def loadSchemas():
    with open("/data/gary/pipeline/schemas/ref_levels.json") as json_file:
        ref_levels = json.load(json_file)
    return ref_levels

#logit = sm.Logit(train['click'],train[train_cols],method='nm',maxiter=1000)
def trainLogistic(data,target,features):
#    try:
    logit = sm.Logit(data[target],data[features])
    result = logit.fit()
    print result.summary()
    return 0
 #   except:
  #      print "error: singular matrix"   
   #     return 1  

def random_subset( iterator, K ):
    result = []
    N = 0

    for item in iterator:
        N += 1
        if len( result ) < K:
            result.append( item )
        else:
            s = int(random.random() * N)
            if s < K:
                result[ s ] = item

    return result 

def main():
    rnd = sys.argv[1]
    ref_levels = loadSchemas()
    refs = []
    for k in ref_levels:
        refs.append(k)
    refs.append('app_category|879c24eb')
    print 'reference levels:'   
    print refs
    df = pd.read_csv('designed.csv',sep=',',low_memory=False)
    #print ref_levels
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    test = df[~msk]  
    train_cols = [col for col in df.columns if 'id' not in col and 'click' not in col]
    train_rand = random_subset(train_cols,rnd)
    #train_rand = ['C16|36','site_category|5378d028','app_category|0f9a328c','C1|1001','device_conn_type|3']
    #train_cols = [col for col in df.columns if 'id' not in col and 'click' not in col and col not in refs]
    trainLogistic(train,'click',train_rand)
    #for col in df[train_rand].columns:
    #    print col
    #print train[train_rand]   
main()



