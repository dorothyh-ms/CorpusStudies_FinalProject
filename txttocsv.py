# convert the output of AntConc to make it more convenient for analysis, including linking with metadata
import os # to make use of commands that are internal to the operating system (os), e.g. dealing with copying files or getting directory paths
import pandas as pd # pandas package is often abbreviated as pd
import shutil # package for facilitating copying/moving files (among other things)
import sys # to get information from terminal (among other system-related properties)
import re # Python package for regular expression handling

# Read the arguments in the command line and assign variable names to them.
# argv[0] is the name of the script you are running
# csvdir is the name of the folder where you have saved the AntConc results as well as the BNC metadata
script, csvdir = sys.argv

# Change directory to the directory where the metadatafile is located
os.chdir(csvdir)

with open("antconc_results_noboothroyd.txt", 'r', encoding="utf8") as sfile:
	with open("temp.csv",'w+', encoding="utf8") as tfile:
		# Provide line with headers for the modified results file
		# Make sure the column containing the file ids has the same column name as it has in the metadata - in this case 'id'
		tfile.writelines("nr\tpre\tmatch-2\tmatch-1\tmatch\tmatch+1\tmatch+2\tpost\tid\n")
		lines=sfile.readlines()
		for line in lines:
			# replace whitespace by tabs for the 3 words preceding and following the first word of the match
			pattern = re.compile("(\w+\W+)(\w+\W+)(\w+\W+)\t(\w+\W+)(\w+\W+)(\w+\W+)(\w+\W+)")
			line = re.sub(pattern,"\g<1>\t\g<2>\t\g<3>\t\g<4>\t\g<5>\t\g<6>\t\g<7>",line)

			pattern = re.compile("\.txt")
			line = re.sub(pattern,"",line)

			tfile.writelines(line)

# read the modified file as a dataframe and put the contents into the variable df ('dataframe')
df = pd.read_csv("temp.csv", encoding="utf8", sep='\t', engine='python')
# Always make sure that the data in the columns that you use as your merge key are in the right format (i.e. str, int, float, ...)
# In this case they are non-numerical characters, which are by default read as strings, so there shouldn't be a problem.
# You might run into trouble though if the ids are numbers (which can be int or float). E.g., to make sure the input is read as a string, you can add:
### df['id'] = df['id'].astype(str) ###

# Read the metadatafile as a dataframe and put the contents into the variable metadf ('dataframe' with metadata)
author_metadata = pd.read_csv("HansardMetaDataAuthors.csv", encoding="utf8", sep='\t', engine='python')
text_metadata= pd.read_csv("HansardMetaDataTexts.csv", encoding = "utf8", sep='\t',engine = 'python')
### metadf['id'] = metadf['id'].astype(str) ###

# Merge the two dataframes using 'id' as key
step1 = pd.merge(df, text_metadata, on='id', how ="left")
step2=pd.merge(step1, author_metadata, left_on = 'display_as', right_on = 'name', how ="left")

# Write dfmerged to new csv-file
step2.to_csv( "mergedresults_withmeta.csv", index=False, sep='\t', encoding='utf8') # no need for an index column, as this has already been provided by AntConc

# Cleaning up: remove the temporary file
os.remove("temp.csv")
