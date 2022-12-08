#!/usr/bin/env python3


import csv
import argparse
from IPython.display import display
from pathlib import Path
import pandas as pd
import numpy as np
import os
import glob
import math
from contextlib import ExitStack


extension = 'csv'
max_markers = 6

# Instantiate the parser
parser = argparse.ArgumentParser(description='Query Genotype Data from Genotype Data Database')

# Input file and string arguments
parser.add_argument("--database", "-d", type=str,
                    help='Specify Genotype Data Database File',required=True)
parser.add_argument("--folder", "-f", type=str,
                    help='Folder containing processed QIAxcel files', required=True)

# Optional arguments
parser.add_argument("--num", "-n", type=int,
                    help='Number of returned results in the query', required=False)
parser.add_argument("--verbose", "-v", action="store_true")
parser.set_defaults(num=3)
parser.set_defaults(verbose=False)

args = parser.parse_args()

# Load Genotype Data Database file
data = pd.read_csv(args.database, sep=',', header=None)
data.columns = ["InternalID",
    "M1", "A1", "A2", "A3", "C1", "C2", "C3",
    "M2", "A4", "A5", "A6", "C4", "C5", "C6",
    "M3", "A7", "A8", "A9", "C7", "C8", "C9",
    "M4", "A10", "A11", "A12", "C10", "C11", "C12",
    "M5", "A13", "A14", "A15", "C13", "C14", "C15",
    "M6", "A16", "A17", "A18", "C16", "C17", "C18",
]
#print(data)

# Split string, [2] for A1, [3] for A2
#query = args.string.split(',')

# Read Folder
path = args.folder
#dir_list = os.listdir(path)
os.chdir(path)
inputFolder = glob.glob('*.{}'.format(extension))
#print(inputFolder)

fileCount = len(inputFolder)
if fileCount > max_markers:
    print("Error: too many markers in input folder.")
    exit()

if fileCount < max_markers:
    print("Caution: there are fewer than 6 input markers in "+args.folder+". Input files: ",fileCount)
    # Allow user to continue but warn that there are fewer markers
    user_input = input('Would you like to continue? (Y/n): ')
    if user_input.lower() == 'n':
        print('Aborting search')
        exit()
    else:
        print('Continuing with ',fileCount,' files.')

# Iterate each file in folder
# for file in inputFolder:
#     inputCSV = pd.read_csv(file)
#     i = np.where(data.values == inputCSV.iloc[1][0])
#     m = i[1][0]
#     a1 = m+1
#     a2 = m+2
#     c1 = m+3
#     c2 = m+4
#
#     # Iterrate each row in file
#     counter = 0;
#     for index, row in inputCSV.iterrows():
#         d1 = row['A1']
#         d2 = row['A2']
#         for index, row2 in data.iterrows():
#             dist = abs(a1 - row2[2]) + abs(a2 - row2[3])
#             #print(dist)
#             #print(counter)
#             counter += 1
#         #dist = abs(a1 - data[2]) + abs(a2 - data[3])
#         #arr_assign(distance,counter,dist)
#         counter += 1

# Open marker files concurrently
with ExitStack() as stack:
    files = [stack.enter_context(open(fname)) for fname in inputFolder]
    # Do something with "files"
    x = len(files)
    inputCSV = []

    # Get rowCount

    rowCount = 96
    for i in range(x):
        inputCSV.append(pd.read_csv(files[i]))
        rowCount = min(rowCount, len(inputCSV[i].index))

    # For each row in input
    # for count in range(rowCount):
    for count in range(4): # Print just 1 row
        # Initialize distance
        data["Distance"] = (0)

        # For each file
        for i in range(x):
            p = np.where(data.values == inputCSV[i].iloc[1][0])
            m = p[1][0]
            a1 = m+1
            a2 = m+2
            c1 = m+3
            c2 = m+4

            d1 = inputCSV[i].iloc[count]['A1']
            d2 = inputCSV[i].iloc[count]['A2']
            e1 = inputCSV[i].iloc[count]['C1']
            e2 = inputCSV[i].iloc[count]['C2']
            # if math.isnan(d1):
            #     d1 = 0
            # if math.isnan(d2):
            #     d2 = 0

            #print(i,": "+inputCSV[i].iloc[1][0])
            #print("d1: ",d1)
            #print("d2: ",d2)
            # Distance calculation
            for index, row in data.iterrows():
                d3 = row.iloc[a1]
                d4 = row.iloc[a2]
                dist = abs(d1 - d3) + abs(d2 - d4)

                # If nan, set 0
                if math.isnan(dist):
                    dist = 0
                # If only one is nan
                if math.isnan(d1) != math.isnan(row.iloc[a1]):
                    dist = 100

                # Concentration ratio modifier;
                if (e1 > e2 and row.iloc[c1] > row.iloc[c2]
                    or e1 < e2 and row.iloc[c1] < row.iloc[c2]
                    or not math.isnan(e1) and math.isnan(e2) and not math.isnan(row.iloc[c1]) and row.iloc[c2]
                    ):
                    dist -= 10
                else:
                    dist += 10
                # Update distance
                data.at[index,"Distance"] += dist
                #print(index)
                #print(data.at[index,"Distance"])
                # if index == 0:
                #     print("d3: ",d3)
                #     print("d4: ",d4)
                #     print("dist",dist)



        #print(count)
        #print(data)
        # print(data.head(args.num))
        if args.verbose:
            print(data.sort_values(by=["Distance"]).head(args.num))
        # for x in data.sort_values(by=["Distance"]).head(args.num).itterows():
            # print(data['InternalID'])


#print(data.sort_values(by=["Distance"]).head(args.num))



# print(query[0])
#a1 = int(query[2])
#a2 = int(query[3])

#print(query)
#print("Querying: A1=" + query[2] + ", A2=" + query[3])
# Print sorted by columns
#print(data.iloc[(data['A1']-a1).abs().argsort()[:10]])
#print(data.iloc[(data['A2']-a2).abs().argsort()[:10]])

# Loop through data, calculate and add new distance column


#print(data.sort_values(by=["Distance"]).head(args.num))
