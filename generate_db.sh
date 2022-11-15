#!/bin/bash

prefix="EXP" # File output name and prefix
np="NP " # No Peak Check

usage() {
   cat << EOF
Usage: generate_db.sh <folder> [, prefix]

  Required
	file Folder containing parse_report.py output files

  [Optional]
  prefix  Internal ID prefix and database output name E.G. "WGS" (default: EXP)

Generates a database output data from parse_report.py for testing.
EOF
   exit 1
}

if [[ ! $# -ge 1 || $# -ge 3 ]]; then
	usage;
fi

# Check directory
files=$(shopt -s nullglob dotglob; echo ${1}output_*.csv)
if (( ${#files} ))
then
  echo "Loading $1"
else
  echo "Error: Directory containing output_*.csv files required. $1 is empty (or does not exist or is a file)"
  exit 1
fi

if [ $# -eq 2 ]; then
  prefix=$2
fi

#for ((i = 0; i < 99; ++i)); do printf -v num '%07d' $i; echo $num; done

cd $1

rm $prefix

# Setup db
for i in {1..94}
do
    count=$(printf "%06d" $i)
    echo ${prefix}$count >> $prefix
done

for f in output_*
do
  echo $f
  counter=1
  while IFS="," read -r -a line; do
    #count=$(printf "%06d" $counter)
    #echo "${prefix}${count},$line" >> $prefix
    append=",${line[0]},${line[2]},${line[3]},${line[4]},${line[5]},${line[6]},${line[7]}"
    sed -i "${counter}s/.*/&${append}/" $prefix
    ((counter+=1))
  done < <(sed '1d;$d' $f)
done
