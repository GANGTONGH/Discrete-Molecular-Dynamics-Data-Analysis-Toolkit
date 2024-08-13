#!/bin/bash

if [[ $# != 3 ]]; then echo "Usage: ./color.sh in_PDB in_param out_colored_PDB"; exit 1; fi

in_PDB=$1
in_param=$2
out_colored_PDB=$3

values=` cat $in_param | awk  -F"E" 'BEGIN{OFMT="%10.02f"} {printf "%.2f", $1 * (10 ^ $2); print ""}' | tr "\n" " " `

awk -v s="$values" 'BEGIN{split(s, a)} {$0 = substr($0,1,62) a[$6] substr($0,67,length($0)); print $0}' $in_PDB > $out_colored_PDB
