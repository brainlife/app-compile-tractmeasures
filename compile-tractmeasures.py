#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import os, sys, argparse
import glob

def concatenateTractData(tsvs,subject,session,tag):

	tractFiles = glob.glob(tsvs+'/*dwi*')
	tractNames = [ f.split('.stat.txt')[0].split('.')[-1:][0] for f in tractFiles ]

	# combine tsvs
	data = pd.DataFrame([],dtype=object)
	tmpdata = pd.read_csv(tractFiles[0],sep='\t',index_col=False,header=None)
	data['measures'] = tmpdata[0]
	data[tractNames[0]] = tmpdata[1]
	for tracts in range(len(tractNames)-1):
		tmpdata = pd.read_csv(tractFiles[tracts+1],sep='\t',index_col=False,header=None)
		data[tractNames[tracts+1]] = tmpdata[1]

	data['subjectID'] = [ subject for f in range(len(data[tractNames[0]])) ]
	data['sessionID'] = [ session for f in range(len(data[tractNames[0]])) ]
	data['tags'] = [ tag for f in range(len(data[tractNames[0]])) ]

	columns = data.columns.tolist()
	columns = columns[-3:] + columns[:-3]
	data = data[columns]

	return data
	
def main():

	print("setting up input parameters")
	#### load config ####
	with open('config.json',encoding='utf-8','r') as config_f:
		config = json.load(config_f)

	#### parse inputs ####
	subjects = [ f['meta']['subject'] for f in config['_inputs'] ]
	sessions = [ f['meta']['session'] for f in config['_inputs'] ]
	tags = [ f['tags'] for f in config['_inputs'] ]
	tsvs = config['tractmeasures']

	#### create and concatenate dataframes for all tracts into single tsv
	if len(tsvs) == 1:
		concat_data = concatenateTractData(tsvs,subjects,sessions,tags)
	else:
		concat_data = pd.DataFrame([],dtype=object)
		for TSVS in range(len(tsvs)):
			#tmp = concatenateTractData(tsvs[TSVS],subjects[TSVS],sessions[TSVS],tags[TSVS])
			concat_data = pd.concat([concat_data,concatenateTractData(tsvs[TSVS],subjects[TSVS],sessions[TSVS],tags[TSVS])])


	#### set up other inputs ####
	# set outdir
	outdir = 'tractmeasures'
	
	# generate output directory if not already there
	if os.path.isdir(outdir):
		print("directory exits")
	else:
		print("making output directory")
		os.mkdir(outdir)

	#### save concatenated data structure ####
	concat_data.to_csv('./tractmeasures/tractmeasure.tsv',sep='\t',index=False)

if __name__ == '__main__':
	main()
