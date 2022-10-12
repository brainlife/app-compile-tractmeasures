#!/usr/bin/env python3

import os,sys
import json
import pandas as pd

def concatenate_csvs(csvs,subjects,sessions,tags,datatype_tags):
    
    data = pd.DataFrame()

    for i in range(len(csvs)):
        # load data
        tmp = pd.read_csv(csvs[i])

        # add subject and session ids if not there
        if 'subjectID' not in tmp.keys().tolist():
            tmp['subjectID'] = [ subjects[i] for f in range(len(tmp)) ]
        if 'sessionID' not in tmp.keys().tolist():
            tmp['sessionID'] = [ sessions[i] for f in range(len(tmp)) ]

        # add tags and datatype tags
        if 'tags' not in tmp.keys().tolist():
            tmp['tags'] = [ tags[i] for f in range(len(tmp)) ]
        if 'datatype_tags' not in tmp.keys().tolist():
            tmp['datatype_tags'] = [ datatype_tags[i] for f in range(len(tmp)) ]

        # concatenate dataframes
        data = pd.concat([data,tmp])
    
    # reset index
    data = data.reset_index(drop=True)

    return data

def main():
    
    # load config
    with open('config.json','r') as config_f:
        config = json.load(config_f)

    # make output directories
    if not os.path.exists('./tractmeasures'):
        os.mkdir('./tractmeasures')

    # set input values
    csvs = config['csv']
    subjects = [ f['meta']['subject'] for f in config['_inputs'] ]
    sessions = [ f['meta']['session'] for f in config['_inputs'] ]
    tags = [ f['tags'] for f in config['_inputs'] ]
    datatype_tags = [ f['datatype_tags'] for f in config['_inputs'] ]

    outPath = './tractmeasures/tractmeasures.csv'

    # concatenate data
    data = concatenate_csvs(csvs,subjects,sessions,tags,datatype_tags)

    # output csv
    data.to_csv(outPath,index=False)

if __name__ == '__main__':
    main()