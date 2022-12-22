#!/usr/bin/env python3


import csv
import argparse
from IPython.display import display
import pandas as pd
import os
import sys


# Instantiate the parser
parser = argparse.ArgumentParser(description='QIAxcel Processing')

# Required arguments
parser.add_argument("--file", "-f", type=str,
                    help='Input QIAxcel File',required=True)
parser.add_argument("--name", "-n", type=str,
                    help='Marker name. Default: File Name', required=True)

# Optional arguments
parser.add_argument("--size", "-s", type=int,
                    help='Reference size n. Default: 400', required=False)
parser.add_argument("--range", "-r", type=int,
                    help='Size range +/- n bp. Default: 150', required=False)
parser.add_argument("--lowerBound", "-l", type=int,
                    help='Overrides lower bound defined by range.', required=False)
parser.add_argument("--upperBound", "-u", type=int,
                    help='Overrides upper bound defined by range.', required=False)
parser.add_argument("--verbose", "-v", action="store_true")
parser.set_defaults(verbose=False)


args = parser.parse_args()
#print("Input File:")
#print(args.file)

# List of valid markers
valid_markers = ['AWRI3', 'AWRI4', 'VRZAG62', 'VVMD2', 'YAG1', 'YAG3']

# Read csv
if args.file is not None:
    data = list(csv.reader(open(args.file)))
    read_height = 14
    rows = len(data)
    samples=int((rows-1)/read_height)
    ref_size = 400 if args.size is None else args.size # Ref size Default: 400
    ref_range = 150 if args.range is None else args.range # Ref range Default: 150
    lBound = (ref_size-ref_range) if args.lowerBound is None else args.lowerBound
    uBound = (ref_size+ref_range+1) if args.upperBound is None else args.upperBound
    size_range = range(max(0,lBound), uBound)
    # print(size_range)
    c_ratio = 0.5 # Concentration ratio
    a_ratio = 0.5 # Ambiguous ratio
    h_ratio = 0.5 # Height ratio

    low_conc = 1.0

    # Check if valid
    if args.name in  valid_markers:
        name = args.name
    else:
        sys.exit("Error: Marker name must be a valid marker: ["+','.join(valid_markers)+']')

    rows = []

    # Constants
    Q_WELL = 1
    Q_HEIGHT = 7    # Height%
    Q_SIZE = 11     # Size
    Q_CONC = 12     # Concentration

    for x in range(0,samples):

        # Loop through picks in sample
        pick_size = len(data[x*read_height+11])
        first_conc=0.0
        first_y=0
        second_conc=0.0
        second_y=0
        third_conc=0.0
        third_y=0
        # Height check
        fourth_hei=0.0
        fourth_y=0
        fifth_hei=0.0
        fifth_y=0

        for y in range(5,pick_size):
            check = data[x*read_height+Q_SIZE][y]
            if check != '' and int(check) in size_range:
                conc = float(data[x*read_height+Q_CONC][y])
                hei = float(data[x*read_height+Q_HEIGHT][y])
                if conc > first_conc:
                    third_y = second_y
                    third_conc = second_conc
                    second_y = first_y
                    second_conc = first_conc
                    first_y = y
                    first_conc = conc
                elif conc > second_conc:
                    third_y = second_y
                    third_conc = second_conc
                    second_y = y
                    second_conc = conc
                elif conc > third_conc:
                    third_y = y
                    third_conc = conc
                # Hei check
                if hei > fourth_hei:
                    fifth_y = fourth_y
                    fifth_hei = fourth_hei
                    fourth_y = y
                    fourth_hei = hei
                elif hei > fifth_hei:
                    fifth_y = y
                    fifth_hei = hei


        # Enforce ratio for haploid
        ratio_check = True if first_conc != 0 and second_conc/first_conc >= c_ratio else False
        ambig_check = True if second_conc != 0 and third_conc/second_conc >= a_ratio else False

        # Check height
        hei_check = False
        if fourth_y != 0:
            # use fifth_y instead if fourth_y is same as first_y
            if fifth_y != 0 and fourth_y == first_y:
                fourth_y = fifth_y
                fourth_hei = fifth_hei
            # Check ratio height
            if first_y != 0:
                first_hei = float(data[x*read_height+Q_HEIGHT][first_y])
                ratio_hei = first_hei/fourth_hei
                if h_ratio <= ratio_hei <= (1/h_ratio):
                    # print("Well: ",data[x*read_height+Q_WELL][Q_WELL])
                    # print(h_ratio, " <= ",ratio_hei, " <= ", 1/h_ratio)
                    hei_check = True

        ## TODO: Add -v verbose option, compare to GrapevineSampleSummaryTable.xlsx column v in GrapeGeneticTest
        #   Add notes field/standard nomenclature e.g.
        #   A2 and A3 are <10% difference Ambiguous 2nd copy A2, etc
        row = [] # Output row
        r0 = name # Source marker name
        r1 = data[x*read_height+Q_WELL][Q_WELL] # Well
        r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = r10 = r11 = ""
        if first_y != 0:
            r2 = data[x*read_height+Q_SIZE][first_y] # A1
            r3 = r2
            r5 = data[x*read_height+Q_CONC][first_y] # C1
            r6 = r5
            r8 = data[x*read_height+Q_HEIGHT][first_y] # H1
            if ratio_check and second_y != 0:
                rTemp = data[x*read_height+Q_SIZE][second_y]
                if hei_check and second_y == fourth_y:
                    r11 += "CP " # Both peakheight and concentration match
                else:
                    r11 += "C "
                if rTemp < r2: # Re-order based on size for human readability
                    r2 = rTemp # A1
                    r6 = r5 # C2
                    r5 = data[x*read_height+Q_CONC][second_y] # C1
                    r9 = r8 # H2
                    r8 = data[x*read_height+Q_HEIGHT][second_y] # H1
                else:
                    r3 = rTemp # A2
                    r6 = data[x*read_height+Q_CONC][second_y] #C2
                    r9 = data[x*read_height+Q_HEIGHT][second_y] # H2
                if ambig_check and third_y != 0:
                    r4 = data[x*read_height+Q_SIZE][third_y] # A3
                    r7 = data[x*read_height+Q_CONC][third_y] # C3
                    r10 = data[x*read_height+Q_HEIGHT][third_y] # H3
                    r11 += "A2 "
            elif hei_check:
                rTemp = data[x*read_height+Q_SIZE][fourth_y]
                if rTemp < r2:
                    r2 = rTemp # A1
                    r6 = r5 # C2
                    r5 = data[x*read_height+Q_CONC][fourth_y] # C1
                    r9 = r8 # H2
                    r8 = data[x*read_height+Q_HEIGHT][fourth_y] # H1
                else:
                    r3 = data[x*read_height+Q_SIZE][fourth_y] # A2
                    r6 = data[x*read_height+Q_CONC][fourth_y] # C2
                    r9 = data[x*read_height+Q_HEIGHT][fourth_y] # H1
                r11 += "P "
        else:
            r11 += "NP "

        # Comments
        if r5 != "" and float(r5) < low_conc:
            r11 += "LC "


        row.extend([r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11])

        rows.append(row)


    df = pd.DataFrame(rows, columns = ["Source", "Well", "A1", "A2", "A3", "C1", "C2", "C3", "H1", "H2", "H3", "Notes"])
    # Print
    if args.verbose:
        print (name," (",size_range,")")
        display(df.to_string())
    fileName = str(f'{os.path.split(args.file)[0] + "/output_" + os.path.split(args.file)[1]}')
    df.to_csv(fileName,index=False)
