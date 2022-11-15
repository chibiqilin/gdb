#!/usr/bin/env python3


import csv
import argparse
from IPython.display import display
from pathlib import Path
import pandas as pd


# Instantiate the parser
parser = argparse.ArgumentParser(description='Insert Genotype Data')

# Input file argument
parser.add_argument("--file", "-f", type=str,
                    help='Specify Database File',required=False)
parser.set_defaults(file="db")
parser.add_argument("--verbose", "-v", action="store_true")
parser.set_defaults(verbose=False)

# Column Parameters & Defaults
# required
parser.add_argument("--species", "-s", type=str,
                    help='Specify Species',required=True)
#parser.set_defaults(species="")
parser.add_argument("--clone", "-x", type=str,
                    help='Specify Clone',required=True)
#parser.set_defaults(clone="")
parser.add_argument("--loc", "-l", type=str,
                    help='Specify genoLoc',required=True)
#parser.set_defaults(loc="")
parser.add_argument("--id", "-k", type=str,
                    help='Specify interal ID for genotype sample info E.g. EXP000001',required=True)
#parser.set_defaults(id="")

# optional
parser.add_argument("--samp", "-b", type=str,
                    help='Specify SampAcc ID',required=False)
parser.set_defaults(samp="")
parser.add_argument("--proj", "-p", type=str,
                    help='Specify ProjAcc ID',required=False)
parser.set_defaults(proj="")
parser.add_argument("--subspec", "-m", type=str,
                    help='Specify SubSpec',required=False)
parser.set_defaults(subspec="")
parser.add_argument("--name", "-n", type=str,
                    help='Specify samName',required=False)
parser.set_defaults(name="")
parser.add_argument("--isolate", "-o", type=str,
                    help='Specify Isolate',required=False)
parser.set_defaults(isolate="")
parser.add_argument("--cultivar", "-c", type=str,
                    help='Specify Cultivar',required=False)
parser.set_defaults(cultivar="")
parser.add_argument("--eco", "-e", type=str,
                    help='Specify ecoType',required=False)
parser.set_defaults(eco="")
parser.add_argument("--geno", "-g", type=str,
                    help='Specify genoType',required=False)
parser.set_defaults(geno="")
parser.add_argument("--age", "-a", type=str,
                    help='Specify Age',required=False)
parser.set_defaults(age="")
parser.add_argument("--dev", "-d", type=str,
                    help='Specify devStage',required=False)
parser.set_defaults(dev="")
parser.add_argument("--sex", "-y", type=str,
                    help='Specify Sex',required=False)
parser.set_defaults(sex="")
parser.add_argument("--gps", "-z", type=str,
                    help='Specify GPS',required=False)
parser.set_defaults(gps="")
parser.add_argument("--tissue", "-t", type=str,
                    help='Specify Tissue',required=False)
parser.set_defaults(tissue="")
parser.add_argument("--provider", "-j", type=str,
                    help='Specify bioProvider',required=False)
parser.set_defaults(provider="")
parser.add_argument("--inst", "-i", type=str,
                    help='Specify authorInst',required=False)
parser.set_defaults(inst="")
parser.add_argument("--date", "-q", type=str,
                    help='Specify Date',required=False)
parser.set_defaults(date="")


args = parser.parse_args()


# Database output:
# Sample accession, Species (mostly vitis vinifera), Subspecies, sample name,
# Cultivar, Clone (missing if applicable), ecotype, genotype, age,
# Developmental Stage, Sizes
# Dr. Liang will provide size for reference (6 numbers), sample information,
# 2 sets of data: experimental and theoretical (insilico/computational) datasets


# Read db, currently stored as flat file csv, alternatively consider relational db like sqlite
# or convert csv to table entry at a later point.

if args.file is not None:
    path = Path(args.file)
    if path.is_file():
        df = pd.read_csv(args.file)
        print(f'Opening {args.file}.')
    else:
        df = pd.DataFrame(columns = ["SampAcc", "ProjAcc", "Species", "subSpec", "samName", "Isolate", "Cultivar", "Clone", "ecoType", "genoType", "Age", "devStage", "Sex", "genoLoc", "GPS", "Tissue", "bioProvider", "authorInst", "Date", "internalID"])


    in_row = {'SampAcc':args.samp, 'ProjAcc':args.proj, 'Species':args.species, 'subSpec':args.subspec, 'samName':args.name, 'Isolate':args.isolate, 'Cultivar':args.cultivar, 'Clone':args.clone, 'ecoType':args.eco, 'genoType':args.geno, 'Age':args.age, 'devStage':args.dev, 'Sex':args.sex, 'genoLoc':args.geno, 'GPS':args.gps, 'Tissue':args.tissue, 'bioProvider':args.provider, 'authorInst':args.inst, 'Date':args.date, 'internalID':args.id}


    df = df.append(in_row, ignore_index=True)

    if args.verbose:
        display(df.to_string())

    df.to_csv(args.file,index=False)
