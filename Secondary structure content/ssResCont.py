# -*- coding: utf-8 -*-""
# Count SSEs for dssp.dat of 5 segments
# Check: n_chains in get_dssp, in final print

import numpy as np
import os
import re
import sys
import argparse
from argparse import RawTextHelpFormatter

script_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(prog='python script.py',
        description="Secondary structure element (SSE) contents for each residue. \n\n\
Columns (left to right): \n\
\talpha-helix; isolated beta bridge; beta-sheet; 3_10 helix; pi-helix; beta-turn; bend; random coil\n\
Rows:\n\
\tresidues",
        formatter_class = RawTextHelpFormatter)
parser.add_argument('-i', '--inDSSP', type=str, help="Input path of DSSP file")
parser.add_argument('-o', '--outSSECont', type=str, help="Output path of SSE contents")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

in_dssp_filename = args.inDSSP
out_filename = args.outSSECont

# Row for one res, cols for SSE's

# Get SSE seq from dssp.dat
def get_dssp(s):
    if s[0] != '#': 
        sse = re.sub(r'[0-9]|!|\n| +', '', s.split()[1])
        return sse
    else:
        return ''
    
# Get SSE of res on each chain, in matrix form; translate to nu. code
def ss_res(seq):
    l_seq = len(seq)
    ss_seq = np.array([[0 for col in range(8)] for row in range(l_seq)])
    char2nu = ''.maketrans('HBEGITSC', '01234567')
    seq_nu = list(map(int,list(seq.translate(char2nu))))

    for i in range(len(seq_nu)):
        ss_seq[i][seq_nu[i]] += 1
    return np.matrix(ss_seq)
        
# Print a 2D list
def print_2d(l_2d, out):
    shape = np.shape(l_2d)
    for i in range(shape[0]):
        for j in range(shape[1]):
            print(l_2d[i][j], file=out, end='\t')
        print('\n', file=out, end='')
    return 0

with open(in_dssp_filename, 'r') as in_dssp_file, open(out_filename, 'w+') as out_file:
    dssp = list(map(get_dssp, in_dssp_file.readlines()))
    sse_cont = np.array([ ss_res(dssp_fr) for dssp_fr in dssp if len(dssp_fr) > 0 ])
    
    result = np.mean(sse_cont,axis = 0, dtype=np.float32).tolist()
    print_2d(result, out_file)
