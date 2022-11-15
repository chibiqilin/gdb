#!/bin/bash

usage() {
   cat << EOF
Usage: sample_n_lines.sh <n> <file>

  n: number of lines to sample
  file: output file from parse_report.py

Takes n randomly sampled lines from parsed QIAxcel data
EOF
   exit 1
}

if [ $# -ne 2 ]; then
	usage;
fi

re='^[0-9]+$'
if ! [[ $1 =~ $re ]] ; then
   echo "Error: n is not a number" >&2; exit 1
fi

if [ ! -f $2 ]; then
  echo "Error: $2 is not a file"
  exit 1
fi

lines=$1
#input_file=/usr/share/dict/words # Test with random words
input_file=$2

# Remove first/last line | remove lines containing "NP " | sort | return first n lines
<$input_file sed '1d;$d'| grep -v "NP " | sort -R | head -n $lines
