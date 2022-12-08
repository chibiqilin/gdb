#!/bin/bash

prefix="EXP" # File output name and prefix

usage() {
   cat << EOF
Usage: generate_db.sh <folder> [, prefix]

  Required
	folder Folder containing parse_report.py output files

  [Optional]
  prefix  Internal ID prefix and database output name E.G. "WGS" (default: EXP)

Generates a database output data from parse_report.py for testing.
EOF
   exit 1
}


if [[ ! $# -ge 1 || $# -ge 3 ]]; then
	usage;
fi

# Check for '/' in folder string
if [[ "$1" == *\/ ]]; then
  folder="$1"
else
  folder="$1/"
fi

# Check directory
files=$(shopt -s nullglob dotglob; echo ${folder}output_*.csv)
if (( ${#files} ))
then
  echo "Loading ${folder}"
else
  echo "Error: Directory containing output_*.csv files required. ${folder} is empty (or does not exist or is a file)"
  exit 1
fi

if [ $# -eq 2 ]; then
  prefix=$2
fi

#for ((i = 0; i < 99; ++i)); do printf -v num '%07d' $i; echo $num; done

cd $folder

if [ -f "$prefix" ]; then
  read -p 'Database already exists. Overwrite the file? (y/N): ' yn
  case $yn in
    y* )
      echo "Backing up file.";
      cp "$prefix" "$prefix.$(date +%d%m%Y)";;
    * )
      echo "Exiting.";
      exit 1;;
  esac
fi

# Setup db
for i in {1..94}
do
    count=$(printf "%06d" $i)
    echo ${prefix}$count >> $prefix
done

for f in output_*.csv
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
