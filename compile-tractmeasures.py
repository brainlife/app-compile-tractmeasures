#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import os, sys, argparse
import glob

def concatenateData(tsvs,subject,session,tag):

	# combine tsvs
	data = pd.concat((pd.read_csv(f,sep='\t',index_col=False) for f in tsvs),ignore_index=True)
	data['subjectID'] = subject
	data['sessionID'] = session
	data['tags'] = tag

	columns = data.columns.tolist()
	columns = columns[-3:] + columns[:-3]
	data = data[columns]

	data.to_csv('./tractmeasures/tractmeasure.tsv',sep='\t',index=False)
	
def main():

	print("setting up input parameters")
	#### load config ####
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	#### parse inputs ####
	subjects = [ f['meta']['subject'] for f in config['_inputs'] ]
	sessions = [ f['meta']['session'] for f in config['_inputs'] ]
	tags = [ f['tags'] for f in config['_inputs'] ]
	tsvs = config['tractmeasures']

	#### set up other inputs ####
	# set outdir
	outdir = 'tractmeasures'
	
	# generate output directory if not already there
	if os.path.isdir(outdir):
		print("directory exits")
	else:
		print("making output directory")
		os.mkdir(outdir)

	#### run command to generate csv structures ####
	print("concatenating tractmeasures")
	concatenateData(tsvs,subjects,sessions,tags)

if __name__ == '__main__':
	main()
