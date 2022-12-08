# gdb
Bioinformatic data analysis pipeline and database for grapevine genetic testing.

### QIAxcel Output Preprocessing
QIAxcel output csv files are preprocessed to obtain the peak calls and format the data. This is done using parse_report.py, or can be facilitated with parse_folder.sh for batch processing.

#### parse_report.py
Parses QIAxcel output csv files. Performs a peak call and formats the data for use.
```
usage: parse_report.py [-h] --file FILE [--size SIZE] [--range RANGE] [--lowerBound LOWERBOUND] [--upperBound UPPERBOUND] [--name NAME]
                       [--verbose]
parse_report.py: error: the following arguments are required: --file/-f
```

Example input:
```
$ ./parse_report.py -f 2022-08-02_AWRI3_20220922_182214_Ex.csv -n AWRI3 -l 302 -u 355 
```

- FILE: Input QIAxcel File
- SIZE: Reference size n. Default: 400
- RANGE: Size range +/- n bp. Default: 150
- LOWERBOUND: Overrides lower bound defined by range.
- UPPERBOUND: Overrides upper bound defined by range.
- NAME: Marker name. Default: File Name

#### parse_folder.sh
Parses all QIAxcel output csv files in a given folder. Markers can be predefined in a simple configuration file. When used with the optional configuration file, the user will be prompted for the file index for each entry. When used without, the user will be prompted to define each manually.

```
Usage: parse_folder.sh <folder> [, configFile]

  Required
	file Folder containing QIAxcel output output files to parse

  [Optional]
  prefix  Config file containing marker names, and lower and upper ranges.

Generates a database output data from parse_report.py for testing.
```

Example input:
```
$ ./parse_folder.sh data/ marker_ranges.txt
Loading data/

Index:	File:
[0]:	data/2022-08-02_AWRI3_20220922_182214_Ex.csv
[1]:	data/2022-08-02_VRZAG64_P1_20220922_182626_Ex.csv
[2]:	data/2022-08-04_VVMD2_20220922_174428_Ex.csv
[3]:	data/2022-08-12_VRZAG64_P2R1_20220922_174918_Ex.csv
[4]:	data/2022-08-12_YAG3_20220922_181711_Ex.csv
[5]:	data/2022-08-15_VRZAG62_20220928_155417_Ex.csv
[6]:	data/2022-08-16_YAG1_20220922_180222_Ex.csv
[7]:	data/2022-08-24_AWRI4_20220928_160956_Ex.csv
[8]:	data/2022-09-12_HFRS-YAG3-AWRI3_20220923_154952_Ex.csv
[9]:	data/2022-09-13_HFRS-AWRI4-YAG1_20220922_172519_Ex.csv
[10]:	data/2022-09-13_HFRS-VRZAG64-VVMD2_20220922_172051_Ex.csv
[11]:	data/2022-09-16_VRZAG64_P2R2_20220922_170834_Ex.csv

Select file index for the following markers (or any char to skip):
AWRI1 (302,355): 0
Parsing data/2022-08-02_AWRI3_20220922_182214_Ex.csv.
AWRI4 (309,489): 7
Parsing data/2022-08-24_AWRI4_20220928_160956_Ex.csv.
VRZAG62 (295,343): 5
Parsing data/2022-08-15_VRZAG62_20220928_155417_Ex.csv.
VVVMD2 (350,413): 2
Parsing data/2022-08-04_VVMD2_20220922_174428_Ex.csv.
YAG1 (331,398): 6
Parsing data/2022-08-16_YAG1_20220922_180222_Ex.csv.
YAG3 (340,398): 4
Parsing data/2022-08-12_YAG3_20220922_181711_Ex.csv.

Output:
data/output_2022-08-02_AWRI3_20220922_182214_Ex.csv  data/output_2022-08-15_VRZAG62_20220928_155417_Ex.csv
data/output_2022-08-04_VVMD2_20220922_174428_Ex.csv  data/output_2022-08-16_YAG1_20220922_180222_Ex.csv
data/output_2022-08-12_YAG3_20220922_181711_Ex.csv   data/output_2022-08-24_AWRI4_20220928_160956_Ex.csv

```

- folder: Folder containing QIAxcel output csv files.
- configFile: Text file containing comma separated values of marker name, lower bound, and upper bound

Config File Example:
```
AWRI1,302,355
AWRI4,309,489
VRZAG62,295,343
VVVMD2,350,413
YAG1,331,398
YAG3,340,398
```

If the folder contains output files a warning will be given, and the user will be prompted to delete the files or cancel.
```
Warning! The following files will be deleted:
data/output_2022-08-24_AWRI4_20220928_160956_Ex.csv
Are you sure you want to continue? [y/N] y
Removing files.
```

### Database Generation
Generation of a database using preprocessed files. Constructed using the shell script generate_db.sh.

#### generate_db.sh
Constructs a simple comma separated flat-file text database. A warning is given when there is an existing database, and overwriting will 
```
Usage: generate_db.sh <folder> [, prefix]

  Required
	folder Folder containing parse_report.py output files

  [Optional]
  prefix  Internal ID prefix and database output name E.G. "WGS" (default: EXP)

Generates a database output data from parse_report.py for testing.
```

- folder: Folder containing preprocessed QIAxcel files.
- prefix: Database name and internal ID.

Example input:
```
$ ./generate_db.sh data/ EXP
```
### Database Querying
Query a database returning the top 3 
#### query.py
```
usage: query.py [-h] --database DATABASE --folder FOLDER [--num NUM] [--verbose]
query.py: error: the following arguments are required: --database/-d, --folder/-f
```

- DATABASE: Specify Genotype Data Database File.
- FOLDER: Folder containing processed QIAxcel files. Expected 6 markers, warning will be given if outside of expected range.
- NUM: Number of returned results in the query.

Example input:
```
$ ./query.py -d data/EXP -f input/
```



