#!/bin/bash

if [[ $# < 7 ]]; then echo "Usage: ./script center1 tolerance1 center2 tolerance2 sampling_interval in_pdb output_commands
	- output_commands: if 1, outputs commands for extracting the representative snapshots; if 0, only outputs the position of snapshots"; exit 1; fi

ctr1=$1
tol1=$2
ctr2=$3
tol2=$4
sampling_interval=$5
in_pdb=$6
out_commands=$7

source_dir="/home/gangtoh/projects/bury-ab40/self/association/rexdmd/"
medusa="/home/gangtoh/medusa-1.1/"

#l_t=(`ls -F ../ | grep K/ | grep / | sort -V`)
l_t=(`~/get-tp.sh ../`)

for t_period in ${l_t[@]}
do
	for i_rep in `seq 0 15`
	do
		i_rep_pad=`printf "%03d" $i_rep`
		common_list=(`comm -12 <(awk -v ctr1=$ctr1 -v tol1=$tol1 '{if($0>=ctr1-tol1 && $0<=ctr1+tol1){print NR}}' ../$t_period/$i_rep/qm.dat | sort) <(awk  -v ctr2=$ctr2 -v tol2=$tol2 '{if($0>=ctr2-tol2 && $0<=ctr2+tol2){print NR}}' ../$t_period/$i_rep/hbond/hbondtot.dat | sort)`)
		t_period_n=`echo -n $t_period | head -c -1`

		if [[ ${#common_list[@]} -gt 0 ]]
		then
			for frame in ${common_list[@]}
			do
   
				# SAMPLING INTERVAL and TEMPERATURE filter
				temp=$(awk -v temp_fr=$(( $frame / 10 )) -v rep_col=$(( $i_rep + 2 )) 'NR == temp_fr+2 {print $rep_col}' "$source_dir/${t_period}/RX_TEMP.out" 2>/dev/null)
				if [[ -n "$temp" && "$temp" =~ ^[0-9]*\.?[0-9]+$ ]]; then
					if [[ $(($frame % $sampling_interval)) == 0 && \
						( $(echo "$temp == 0.590" | bc -l) -eq 1 || $(echo "$temp == 0.610" | bc -l) -eq 1 ) ]]; then
						echo $t_period $i_rep $frame `printf "%03d" $i_rep`
					fi
				fi
    
			done
		fi
	done
done > tmp-$ctr1-$tol1-$ctr2-$tol2.dat
if [[ $out_commands == 1 ]]
then
	echo "mkdir $ctr1-$tol1-$ctr2-$tol2/"
	echo "rm $ctr1-$tol1-$ctr2-$tol2/*"
	awk -v sourceDir=$source_dir -v iPDB=$in_pdb -v dir=`pwd` -v c1=$ctr1 -v t1=$tol1 -v c2=$ctr2 -v t2=$tol2 -v Medusa=$medusa '{print "cd " dir "; " Medusa "/src/apps/complex_M2P.linux -P " Medusa "parameter -I " iPDB " -M " sourceDir  "/" $1 "/" $2 "/p" $4 ".rexdmd_movie -o " c1 "-" t1 "-" c2 "-" t2 "/" substr($1, 1, length($1)-1) "." $2 "." $3 ".pdb -F " $3-1 ":1:1 -T ~/ions-new1/topparam"}' tmp-$ctr1-$tol1-$ctr2-$tol2.dat
elif [[ out_commands == 0 ]]
then
	mv tmp-$ctr1-$tol1-$ctr2-$tol2.dat info-$ctr1-$tol1-$ctr2-$tol2.dat
        echo "Position of snapshots saved to info-$ctr1-$tol1-$ctr2-$tol2.dat"
fi
