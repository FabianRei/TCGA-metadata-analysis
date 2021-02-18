import json
from pathlib import Path
from collections import Counter
import re
import pprint
import pickle


metadata_path = Path.cwd()/'data'/'metadata.cart.2021-01-27.json'
with metadata_path.open() as f:
    metadata = json.load(f)

# tumor stage call
# metadata[0]['cases'][0]['diagnoses'][0]['tumor_stage']

# file name call
# metadata[0]['file_name']

# sanity check. Each file should contain only one case..
num_cases = [len(meta['cases']) for meta in metadata]
pp = pprint.PrettyPrinter()
print("Number of cases per file:"); pp.pprint(Counter(num_cases))
# -> only one case per file metadata
# same for diagnoses:
num_diagnoses = [len(meta['cases'][0]['diagnoses']) if 'diagnoses' in meta['cases'][0].keys() else 0 for meta in metadata]
print("Number of diagnoses per file:"); pp.pprint(Counter(num_diagnoses))
# 2 files don't seem of have diagnoses.

# create list with filenames
filenames = [meta['file_name'] for meta in metadata]

# create list with files containing a diagnosis
meta_diagnosis = [meta for meta in metadata if 'diagnoses' in meta['cases'][0].keys()]
# make list with filenames that have a diagnosis for themselves
filenames_diagnosis = [filename for (filename, meta) in zip(filenames, metadata) if 'diagnoses' in meta['cases'][0].keys()]

# check if each diagnosis has tumor stage information
num_tumor_stages = [1 if 'tumor_stage' in meta['cases'][0]['diagnoses'][0] else 0 for meta in meta_diagnosis]
print('Tumor stage in diagnosis data:'); pp.pprint(Counter(num_tumor_stages))
# each file with diagnosis data also has tumor stage in its diagnosis data :)

# get an overview of tumor stages in files
tumor_stages = [meta['cases'][0]['diagnoses'][0]['tumor_stage'] for meta in meta_diagnosis]
print("Various tumor stages are:"); pp.pprint(Counter(tumor_stages))

# regex to extract stage numbering
# re.findall(r'(iv|i{1,3})', 'stage iv')

# check if stage numbering always extracts one or none
num_regex_stages = [len(re.findall(r'(iv|i{1,3})', stage)) for stage in tumor_stages]
print('The number of regex extractions are:'); pp.pprint(Counter(num_regex_stages))
# the 46 stages not found are 'stage x' and 'not reported'

# filter to stage i to iv
filtered_stages = [re.findall(r'(iv|i{1,3})', stage)[0] for stage in tumor_stages if len(re.findall(r'(iv|i{1,3})', stage)) > 0]
print("Looking at stages i to iv, we find the following frequencies:"); pp.pprint(Counter(filtered_stages))
# also filter filenames..
filenames_stage = [filename for filename, stage in zip(filenames_diagnosis, tumor_stages) if len(re.findall(r'(iv|i{1,3})', stage)) > 0]
# create dict that contains filename & stage diagnosis
diagnosis_dict = {filename:stage for filename, stage in zip(filenames_stage, filtered_stages)}

# save diagnosis dict
# with (Path.cwd()/'data'/'diagnosis_dict.pickle').open(mode='wb') as f:
#     pickle.dump(diagnosis_dict, f)
print('d0ne!')

# visualize:
import matplotlib.pyplot as plt
plt.style.use('classic')
plt.style.use('fivethirtyeight')
# swap #1 with #2 for stages to be ordered i to iv:
temp1 = filtered_stages[0]; temp2 = filtered_stages[1]
filtered_stages[0] = temp2; filtered_stages[1] = temp1
plt.hist(filtered_stages)

