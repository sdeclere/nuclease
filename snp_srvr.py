#/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request
from flask import render_template
import glob 
import re

igv_str = "http://localhost:60151/load?file=/Volumes/bioit/Stephane/GFR/VCF2/bams/%s_sorted_sorted_AORRG_realigned_rmdup_realiable.bam&locus=%s:%d-%d&genome=sacSer3&merge=false"

def load_pileups():
    mut_files = glob.glob('./pileups/*.mut_new')
    muts={}
    for f in mut_files:
        pp =open(f,'r').readlines()
        strain = f.split('_')[0]
        for m in pp:
            sm = m.strip().split()
            # add percentage
            if len(sm) <= 4 : 
                sm.append("NO_COV")
                sm.insert(3, 0)
            else : 
                pp = sm[4]
                cov = float(sm[3]) + pp.count('+') + pp.count('-')
                pvar = ((pp.count(',') + pp.count('.'))/cov)*100
                print pp, cov, pvar
                sm.insert(3, '%.2f' % pvar)
            k = (sm[0],sm[1])
            if muts.has_key(k):
                muts[k].append((strain.split('/')[2], sm))
            else:
                muts[k]=[(strain.split('/')[2], sm)]
            sm.append( igv_str % (strain.split('/')[2], sm[0], int(sm[1])-50, int(sm[1])+50 ) )
    return muts

################################################
p= load_pileups() 

## starr web app 
app = Flask(__name__, template_folder='.') 
@app.route('/mutation/<k>/<pos>')
def view_mutation(k,pos):
    return render_template('mut.html', k=k, pos=pos, mut=p[(k,pos)])
    
@app.route('/')
@app.route('/index')
def index():
    m = p.keys()
    return render_template('index.html', muts=sorted(m))
    
if __name__ == '__main__':
    app.run()
