import pandas as pd
import os
import argparse as arg
import sys

parser = arg.ArgumentParser()
parser.add_argument('--files', type=str, help = "Path to directory containing TCGA files.")
parser.add_argument("--file_suffix", type = str, help = "Type of file (bam, tsv, vcf, etc.)")
parser.add_argument('--sample_sheet', type=str, help = "Path to TCGA sample-sheet.")
args = parser.parse_args()

sample_data = pd.read_csv(args.sample_sheet, sep = "\t")

files = os.listdir(args.files)

mapping = {}
for name, id, sample in zip(sample_data["File Name"], sample_data["Case ID"], sample_data["Sample Type"]):
    print(sample)
    if sample == "Primary Tumor" or sample == "Metastatic":
        mapping[name] = f"{id}_T.{args.file_suffix}"
        print("here")
    if sample == "Blood Derived Normal":
        mapping[name] = f"{id}_N.{args.file_suffix}"
print(mapping)

for file in files:
    if file == '.DS_Store':
        continue
    os.rename(f"{args.files}/{file}", f"{args.files}/{mapping[file]}")



