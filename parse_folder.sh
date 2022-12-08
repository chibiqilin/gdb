#!/bin/bash

usage() {
   cat << EOF
Usage: parse_folder.sh <folder> [, configFile]

  Required
	file Folder containing QIAxcel output output files to parse

  [Optional]
  prefix  Config file containing marker names, and lower and upper ranges.

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

# Check for output files, remove if proceeding
files=$(shopt -s nullglob dotglob; echo ${folder}output_*.csv)
if (( ${#files} ))
then
  echo "Warning! The following files will be deleted:"
  echo ${files} | tr ' ' '\n'
  read -r -p "Are you sure you want to continue? [y/N] " response
  case "$response" in
      [yY][eE][sS]|[yY])
          echo "Removing files."
          rm ${files}
          ;;
      *)
          echo "Aborting."
          exit 1
          ;;
  esac
fi


# Check directory if empty
files=$(shopt -s nullglob dotglob; echo ${folder}*.csv)
if (( ${#files} ))
then
  echo "Loading ${folder}"
else
  echo "Error: Directory containing QIAxcel *.csv files required. ${folder}/ is empty (or is not a folder)"
  exit 1
fi

# Check config file
if [ -f "$2" ]; then
  files=(${folder}*.csv)
  echo -e "\nIndex:\tFile:"
  for ((i=0; i<${#files[@]}; i++)); do
    echo -e "[$i]:\t${files[$i]}"
  done
  echo -e "\nSelect file index for the following markers (or any char to skip):"
  while IFS=',' read -ra arr; do
    read -p "${arr[0]} (${arr[1]},${arr[2]}): " fi  </dev/tty
    re='^[0-9]+$' # Check input for int
    if ! [[ $fi =~ $re && ! -z ${files[$fi]} ]] ; then
      echo "Skipping."
    else
      echo "Parsing ${files[$fi]}."
      ./parse_report.py -f ${files[$fi]} -n ${arr[0]} -l ${arr[1]} -u ${arr[2]}
    fi
  done < $2
  echo -e "\nOutput:"
  ls ${folder}output_*
else # Check each filemanually
  for file in ${folder}*.csv
  do
    echo $file
    read -p "Select this marker? (y/N) " yn
    case $yn in
    	y* ) read -p "Marker Name: " nm;
        read -p "Marker lower bound: " lb;
        read -p "Marker upper bound: " ub;
        ./parse_report.py -f $file -n $nm -l $lb -u $ub;
        echo "";;
    	* ) echo "Skipping Marker";
        echo "";;
    esac
  done
fi
