#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import os, sys, argparse
import glob

def concatenateTractData(tsvs,subject,session,tag):

	tractFiles = glob.glob(tsvs+'/*dwi*')
	tractNames = [ f.split('.stat.txt')[0].split('.')[-1:][0] if 'no_result' not in f else f.split('.no_result.txt')[0].split('.')[-1:][0]+'_no_result' for f in tractFiles ]

	# combine tsvs
	data = pd.DataFrame([],dtype=object)
	no_result_cnt = ''
	while no_result_cnt == '':
		for tracts in range(len(tractNames)):
			if 'no_result' not in tractNames[tracts]:
				no_result_cnt = tracts
				break

	tmpdata = pd.read_csv(tractFiles[no_result_cnt],sep='\t',index_col=False,header=None)
	data['measures'] = tmpdata[0]
	data[tractNames[0]] = tmpdata[1]
	for tracts in range(len(tractNames)):
		if tracts != no_result_cnt:
			if 'no_result' not in tractNames[tracts]:
				tmpdata = pd.read_csv(tractFiles[tracts],sep='\t',index_col=False,header=None)
				data[tractNames[tracts]] = tmpdata[1]
			else:
				tmpdata[1] = [ np.nan for f in range(len(tmpdata[0])) ]
				data[tractNames[tracts].split('_no_result')[0]] = tmpdata[1]

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
	with open('config.json',encoding='utf-8') as config_f:
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
			print(TSVS)
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
