import pandas as pd
import os
import argparse as arg

# Add command line arguments
parser = arg.ArgumentParser()
parser.add_argument('--files', type=str, help = "Path to directory containing TCGA files.")
parser.add_argument("--file_suffix", type = str, help = "Type of file (bam, tsv, vcf, etc.)")
parser.add_argument('--sample_sheet', type=str, help = "Path to TCGA sample-sheet.")
args = parser.parse_args()

# Read sample sheet 
sample_data = pd.read_csv(args.sample_sheet, sep = "\t")

# List files in directory
files = os.listdir(args.files)

# Create empty dictionary for use in ID mapping
mapping = {}

# Iterate over files in sample sheet and create our lab ID from metadata and map to file id from samples sheet
for name, id, sample in zip(sample_data["File ID"], sample_data["Case ID"], sample_data["Sample Type"]):
    if sample == "Primary Tumor" or sample == "Metastatic":
        mapping[name] = f"{name}_{id}_T.{args.file_suffix}"
    if sample == "Blood Derived Normal":
        mapping[name] = f"{name}_{id}_N.{args.file_suffix}"

# Iterate over files, ignoring .DS_Store, and rename them according to the dictionary mapping.
for file in files:
    if file == '.DS_Store':
        continue
    os.rename(f"{args.files}/{file}", f"{args.files}/{mapping[file.split("_")[0]]}")



