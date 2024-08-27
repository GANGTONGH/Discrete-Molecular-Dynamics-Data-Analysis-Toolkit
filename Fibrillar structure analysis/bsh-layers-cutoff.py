#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 19:45:55 2022

@author: gh
"""

import os
import re
import argparse
from argparse import RawTextHelpFormatter

script_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(prog='python SCRIPT.py',
         description="beta-sheet number in the largest Beta-sheet cluster, excluding the cases where max_beta-sheet-clusterSize are below cutoff \n",
formatter_class = RawTextHelpFormatter)

parser.add_argument('-dssp', '--in_DSSP', type=str, help="Input path of DSSP file")
parser.add_argument('-bshClust', '--in_bshClust', type=str, help="Input path of group_rg file (from -b of Medusa COMPLEX_ANALYSIS)")
parser.add_argument('-o', '--out_betasheet_layers', type=str, help="Output path of beta-sheet number and size")
parser.add_argument('-c', '--cutoff', type=int, help="Cutoff of smallest cluster size to be considered in the analysis. 0 for NO cutoff and considering all clusters")
parser.add_argument('-v', '--valid_chains', type=str, help="Index of chains to be counted in cluster, in standard Python list format as a string. NO WHITESPACE. Example: \"[1,2,3,4]\" ")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

in_filename_1 = args.in_DSSP
in_filename_2 = args.in_bshClust
out_filename = args.out_betasheet_layers
clustSizeCutoff = args.cutoff

if args.valid_chains == None: exit(1)
valid_chains = eval(args.valid_chains)

def strip_lines(file_lines):
    stripped_lines = [ s.strip('\n') for s in file_lines ]
    return stripped_lines

# Get beta-sheep info from a line in dssp.dat
def get_bsh_info(s):
    if s[0] == '#': 
        return ''
    else:
        bsh_info = re.split(r' +', s.strip('\n'))[2:]
        return ' '.join(bsh_info)

# Count occurance of members of l_ref in l
def count_occur(l,l_ref):
    i = 0
    for elem in l:
        if elem in l_ref:
            i = i + 1
        else:
            continue
    return i

def cluster_size_max(clean_line, N):
    clusters = [ elem for elem in clean_line.split(' ') if elem != '' ][1:]
    chains = [ re.split(r'[,]+', cluster) for cluster in clusters ]

    clustersize = [ count_occur(map(int,l),valid_chains) for l in chains ]
    max_cs = max(clustersize)
    max_mwcs = (max_cs ** 2) / N

    max_cluster = [ int(elem)+1 for elem in chains[clustersize.index(max(clustersize))] if int(elem)+1 in valid_chains ]
    
    return max_mwcs, max_cluster

def n_bsh_chains(s_bsh):
    N_bsh_chains = len(re.split(r'-|,|\.', s_bsh)[::4])
    # print(N_bsh_chains)
    return N_bsh_chains

# B-sheets in max-cluster!
def bsh_size_mw_maxcluster(s_clu, s_bsh, N_bsh_chains):

    sheets = [ substr for substr in s_bsh.split(' ') if substr != '' ]

    max_mwcs, max_clu = cluster_size_max(s_clu, N_bsh_chains)

    # Number of b-strands in b-sheet
    n_strands = 0
    # Total b-sh strand number in max-cluster
    N_strands = 0

    for sheet in sheets:
        strands = [ int(elem) for elem in re.split(r'-|,|\.|:|\ ', sheet)[::4] if elem != '' and elem[0].isnumeric() ]
        if (all(x in max_clu for x in strands)): n_strands = n_strands + len(strands)**2; N_strands = N_strands + len(strands)

    if ( N_strands < clustSizeCutoff or N_strands == 0 ): return ''
    else:
        # Mean b-sh size in largest cluster, mass-weighted
        # print(N_strands, N_bsh_chains)
        n_strands_mean = n_strands / N_strands
        n_bsh_in_maxclu = len(max_clu) / n_strands_mean 
        # Number of b-sheets in max_cluster, avg. umber of strands in a b-sheet
        return n_bsh_in_maxclu, n_strands_mean

with open(in_filename_1, 'r') as in_file_1, open(in_filename_2, 'r') as in_file_2, open(out_filename, 'w+') as out_file:
    # 1: dssp; 2: bsh.dat

    data_1 = in_file_1.readlines()
    data_2 = in_file_2.readlines()
    
    data_clean_1 = [get_bsh_info(s) for s in strip_lines(data_1)]
    data_clean_2 = strip_lines(data_2)

    for i in range(min(len(data_clean_1), len(data_clean_2))):
        if data_clean_1[i] != '' : 
            n_tot_bshChains = n_bsh_chains(data_clean_1[i])
        else: 
            continue
        
        result = bsh_size_mw_maxcluster(data_clean_2[i], data_clean_1[i], n_tot_bshChains)
        if result != '': print(result[0], result[1], file=out_file)
    
    in_file_1.close(); in_file_2.close(); out_file.close()
