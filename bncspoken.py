# create BNC subcorpus selecting spoken texts only
import os # to make use of commands that are internal to the operating system (os), e.g. dealing with copying files or getting directory paths
import pandas as pd # pandas package is often abbreviated as pd
import shutil # package for facilitating copying/moving files (among other things)
import sys # to get information from terminal (among other system-related properties)

# Read the arguments in the command line and assign variable names to them. 
# argv[0] is the name of the script you are running
script, csvdir, inputdir, outputdir = sys.argv 

# Change directory to the directory where the metadatafile is located
os.chdir(csvdir)

# Read the metadatafile as a dataframe and put the contents into the variable df ('dataframe')
df = pd.read_csv("bnc_metadata_utf8.csv", encoding="utf8", sep='\t', engine='python')

# Define subset using pandas 'loc' (locate rows based on labels, i.e. cell values) 
# in combination with 'contains' to match partial cell values
subset = df.loc[df['text_type'].str.contains("spoken"), 'id']
# A less precise subset is for instance one 
# that matches a specific cell value containing 'spoken', such as "spoken_context"
### subset = df.loc[df['text_type'] == "spoken_context", 'id'] ###
# Using isin (a list of items) you can also use this technique to create the same filter
### subset = df.loc[df['text_type'].isin(["spoken_context","spoken_demographic","written-to-be-spoken"]), 'id'] ###

# Put  files that are in inputdir (the full corpus) in a list called 'files'
files = os.listdir(inputdir)

# start a loop where you copy every file that meets the condition 'spoken' to a new folder (which you created prior to running the script)
for ids in subset:
	src = os.path.join(inputdir, ids+".txt")
	dest = os.path.join(outputdir, ids+".txt")
	shutil.copy2(src,dest)

