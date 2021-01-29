import pickle
from pathlib import Path
import numpy as np

# path to dict that has stage information (stage i to iv), as well as path to filenames of downloaded .svs files
path_filenames = Path.cwd()/'data'/'filenames.txt'
path_diagnosis_dict = Path.cwd()/'data'/'diagnosis_dict.pickle'

# open files
with path_filenames.open() as f:
    filenames = f.read().splitlines()

with path_diagnosis_dict.open(mode='rb') as f:
    diagnoses = pickle.load(f)

# all filenames of diagnoses we have
diagnoses_filenames = [*diagnoses]

# look at intersection to determine, whether all files, for which I have a diagnosis, also are downloaded already :)
result = np.intersect1d(filenames, diagnoses_filenames)
# results in intersection are of lenth 1930. Which more files are needed?
needed_files = [filename for filename in diagnoses_filenames if filename not in filenames]
# TCGA-AR-A1AI-01A-01-TSA.b560bb34-c0c8-497b-8508-c3a2929f9ece.svs isn't found within the TCGA database. It's fortunately
# not a stage iv cases (it's stage ii), so I'll work without it.

# new runs should now only find the above case missing
print('Missing svs files with valuable diagnosis:', needed_files)

print('d0ne')
