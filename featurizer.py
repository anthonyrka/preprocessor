#!/usr/local/bin/python

import io
import json
import csv
import pandas as pd
import numpy as np
import operator

RESPONSE_POSITION = 2
ID_POSITION = 1
DELIMITER =','
INFILE = 'train_sample.csv'
LIM = 1000000

def loadSchemas():
    with open("/data/gary/pipeline/schemas/positions.json") as json_file:
        pos = json.load(json_file)

    with open("/data/gary/pipeline/schemas/types.json") as json_file:
        types = json.load(json_file)

    with open("/data/gary/pipeline/schemas/levels.json") as json_file:
        levels = json.load(json_file)
    
    return pos,types,levels

def saveJSON(obj,file_name):
    path = '/data/gary/pipeline/schemas/%s.json' % (file_name)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(obj, ensure_ascii=False)))
    return None

def getDummies(file_name,pos_map,level_map,rpos,pos,rnpos,npos):
    ifile = csv.reader(open(file_name,'rb'),delimiter=DELIMITER)
    ifile.next()
    
    i=1
    ofile = open('designed.csv','wb')
    #print new_line
    #for k,v in rnpos.iteritems():
    #    print k,v
    w = csv.DictWriter(ofile,delimiter=',',fieldnames=npos.keys())
    w.writeheader()

    for line in ifile:


        if i > LIM:
            pass

        else:
            #print line

            k = 1
            new_line = {}
            line_map = {}
            for l in line:
                line_map[k] = l
                k+=1


            for key,val in sorted(line_map.items(), key=operator.itemgetter(0)):

                if int(key) not in pos_map.keys():

                    pass
                else:

                    prange = pos_map[key]
                    if(len(prange) == 1):
                        field_name = "%s|%s" % (str(pos[str(key)]),val)
                        #new_line[key] = val
                        new_line[rnpos[int(key)]] = val
                    else:
                        for x in prange.split('|'):
                            if x == '':
                                pass
        
                            else:
       
                                lm_key = "%s|%s" % (str(pos[str(key)]),val)


                                old,new = level_map[lm_key].split('|')

                                if(new==x):
                                    new_line[rnpos[int(x)]] = 1
                                else:
                                    new_line[rnpos[int(x)]] = 0

            w.writerow(new_line)


        i+=1
    return None
      

def main():
    print '******CREATING DESIGN VARIABLES******'
    pos,types,levels = loadSchemas()

    rpos = {}
    for k,v in pos.iteritems():
        rpos[v] = k

    npos = {}
    rnpos = {}
    npos[pos[str(ID_POSITION)]] = 1
    npos[pos[str(RESPONSE_POSITION)]] = 2
  
    pos_map = {}
    level_map = {}
    xpos_range = {}
    opos = {}
    i=3
    ref_level = {}
    for key,val in levels.iteritems():
        if val == 'too many levels':
            pass
        else:
            j=''
            k = 0
            for v in val:
                newcol = "%s|%s" % (key, v)
                npos[newcol] = i            
                #rnpos[i] = newcol
                opos[newcol] = int(rpos[key])
                old_new = "%s|%s" % (rpos[key],str(i))
                level_map[newcol] = old_new
                j = j + str(i) + '|'
                if(k==0):
                    ref_level[newcol] = key
                k+=1
                i+=1
            xpos_range[key] = j
            pos_map[int(rpos[key])] = j
    pos_map[ID_POSITION] = str(ID_POSITION)
    pos_map[RESPONSE_POSITION] = str(RESPONSE_POSITION)
    for k,v in npos.iteritems():
        rnpos[v] = k
#    for k,v in sorted(rnpos.items(), key=operator.itemgetter(0)):
 #       print k,v
    getDummies(INFILE,pos_map,level_map,rpos,pos,rnpos,npos)
    #for k,v in sorted(level_map.items(),key=operator.itemgetter(0)):
    #    print k,v
    #print '****ref levels****'
    #for k,v in ref_level.iteritems():
    #    print k,v
    saveJSON(ref_level,'ref_levels')
main()
