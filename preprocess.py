#!/usr/local/bin/python

import io
import os
import sys
import string
import json

sys.path.append("/data/gary/pipeline/schemas")

RESPONSE_POSITION = 2
ID_POSITION = 1
DELIMITER =','
SAMPLEMAX = 1000000
P = float(sys.argv[2])
#TOSS = 0.0002
TOSS = 0.0001
RMTYPES = "double_precision"

def checkSample(file_name):
    #wc = "wc -l %s" % (file_name)
    #lines = os.popen(wc).read()
    lines = '40428968 train'
    lines = lines.split()[0]
    if lines > SAMPLEMAX:
        ofile = 'train_sample.csv'
        #cmd = "bash sample.sh %s %s %f" % (file_name,ofile,P)
        #os.popen(cmd)
        wc = "wc -l %s" % (ofile)
        lines = os.popen(wc).read().split()[0]
    else:
        ofile = file_name
    print 'new file: ' + ofile
    print lines
    return ofile,lines

def typeVars(file_name):
    cmd = """awk -F%s -f %s %s""" % (DELIMITER,'typevars.awk',file_name)
    out = os.popen(cmd).read()
    return out

def cutLevels(file_name,col):
    cmd = """cut -d %s -f%d %s | sort | uniq -c """ % (DELIMITER,col,file_name)
    out = os.popen(cmd).read()
    return out

def fieldMap(fields):
    types = {}
    pos = {}
    i=1
    for f in fields:
        var,dtype = f.split()
        types[var] = dtype
        pos[i] = var
        i+=1
    return types,pos

def saveJSON(obj,file_name):
    path = '/data/gary/pipeline/schemas/%s.json' % (file_name)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(obj, ensure_ascii=False)))
    return None

def getLevels(file_name,types,pos,lines):
    levels = {}
    L_T = string.Template("""\"$var\": \"$freqs\"""")
    for x in xrange(len(types.keys())):
        print "Searching for levels on : %s" % (pos[x+1])


        if(x+1==ID_POSITION or x+1==RESPONSE_POSITION or types[pos[x+1]].find(RMTYPES) != -1):

            pass
        else: 
            data = cutLevels(file_name,x+1).strip().split('\n')
            #name = '/data/schemas/levels.' + str(x+1) + '.' + pos[x+1] + '.txt'
            #with io.open(name, 'w', encoding='utf-8') as f:
            #    f.write(unicode(data))
            print "Found %d levels" % (len(data))

            val_freq = [] 
            j=1
            for d in data:
                vals = d.strip().split()
                val,freqs = vals[1],vals[0]
                if(val in types.keys()):
                    pass
                else:
                    v = L_T.substitute(var=val,freqs=freqs)
                    val_freq.append(v)
                j+=1
            #print j,TOSS
            print "levels: %d, lines %s, toss: %f, perc %f" % (j,lines,TOSS,float(j)/float(lines))
            print 'percent of lines: ',str(float(j)/float(lines))
            if((float(j)/float(lines)) < TOSS):
                level_map = ','.join(val_freq)
                level_map = '{' + level_map + '}'

                lvl = json.loads(level_map)
           # name = 'levels.' + str(x+1) + '.' + pos[x+1]   
                levels[pos[x+1]] = lvl
                print "%d Below toss threshold" % (j)
            else:
                levels[pos[x+1]] = 'too many levels'
                print "%d Above toss threshold." % (j)
    return levels
   
def main():
    print '******BEGIN: PREPROCESSING*******'
    f = sys.argv[1]
    f,lines = checkSample(f)

    types,pos = fieldMap(typeVars(f).strip().split(DELIMITER))
    
    print "Total columns found: %d" % (len(types.keys()))
    saveJSON(pos,'positions')
    saveJSON(types,'types')
    levels = getLevels(f,types,pos,lines)
    saveJSON(levels,'levels')

 
main()
