#!/bin/bash


usage() {
   cat << EOF
Usage: compare_picks.sh <file1> <file2>

	file1:	Pick module output csv
	file2:	GrapevineSampleSummaryTable csv page

Compared picks from file1 and file2
EOF
   exit 1
}

if [ $# -ne 2 ]; then
	usage;
fi

if [[ ! -f $1 ]]; then
    echo "$1 does not exist on your filesystem."
    exit 1
fi

if [[ ! -f $2 ]]; then
    echo "$2 does not exist on your filesystem."
    exit 1
fi

file1=$1
file2=$2
linecount=$(wc -l $file1 | awk '{print $1;}')
header=$(head -n1 $file1)
echo $header

for (( i=2 ; ((i-($linecount+1))) ; i=(($i+1)) ))
do
	j=$((i-1))
	line1=$(sed "${i}q;d" $file1)
	line2=$(sed "${j}q;d" $file2)
	a1=$(echo $line1 | awk -F\, '{ print $3 }')
	a2=$(echo $line1 | awk -F\, '{ print $4 }')
	b1=$(echo $line2 | awk -F\, '{ print $1 }')
	b2=$(echo $line2 | awk -F\, '{ print $2 }')
	#echo $a1 $a2
	#echo $b1 $b2
	a=$((a1 + a2))
	b=$((b1 + b2))
	if [ "$a" -ne "$b" ]; then
		echo $line1
	fi
done;
