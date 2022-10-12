#!/usr/bin/env python3

import os,sys
import json
import requests
import pandas as pd

## this will add a subjectID and sessionID column to the output data
def add_subjects_sessions(subject,session,path,data):
    
    if 'subjectID' not in data.keys():
        data['subjectID'] = [ str(subject) for f in range(len(data)) ]
    
    if 'sessionID' not in data.keys():
        data['sessionID'] = [ str(session) for f in range(len(data)) ]
        
    return data

## this function calles check_for_duplicates and attempts to find duplicates. then uses that output, sets a dumby sessionID if not present,
## and appends the object data
def append_data(subjects,sessions,paths,finish_dates,obj,filename):
        
    # check for duplicates. if so, remove
    finish_dates, subjects, sessions, paths = check_for_duplicates(obj,finish_dates,subjects,sessions,paths)

    # append data to appropriate lists
    subjects = np.append(subjects,str(obj['output']['meta']['subject']))
    if 'session' in obj['output']['meta'].keys():
        sessions = np.append(sessions,obj['output']['meta']['session'])
    else:
        sessions = np.append(sessions,'1')
    paths = np.append(paths,"input/"+obj["path"]+"/"+filename)
    finish_dates = np.append(finish_dates,obj['finish_date'])
    
    return finish_dates, subjects, sessions, paths

## this function will call add_subjects_sessions to add the appropriate columns and will append the object data to a study-wide dataframe
def compile_data(paths,subjects,sessions,data):
    # loops through all paths
    for i in range(len(paths)):
        # if network, load json. if not, load csv
        if '.json.gz' in paths[i]:
            tmpdata = pd.read_json(paths[i],orient='index').reset_index(drop=True)
            tmpdata = add_subjects_sessions(subjects[i],sessions[i],paths[i],tmpdata)
        else:
            if '.tsv' in paths[i]:
                sep = '\t'
            else:
                sep = ','
            tmpdata = pd.read_csv(paths[i],sep=sep)
            tmpdata = add_subjects_sessions(subjects[i],sessions[i],paths[i],tmpdata)

        data = data.append(tmpdata,ignore_index=True)

    # replace empty spaces with nans
    data = data.replace(r'^\s+$', np.nan, regex=True)
    
    return data

# this function will comile network adjacency matrices into a dictionary structure
def compile_network_adjacency_matrices(paths,subjects,sessions,data):
    
    # loop through paths and append adjacency matrix to dictionary
    for i in range(len(paths)):
        data[subjects[i]+'_sess'+sessions[i]] = jgf.conmat.load(paths[i],compressed=True)[0]

    return data

### load data
## this function is useful for identifying duplicate datatypes. if it finds one, it will update the data with the latest finishing dataset.
def check_for_duplicates(obj,finish_dates,subjects,sessions,paths):
    
    # first checks if there is a session id available in the keys of the object. if finds one, then checks if the subject and session ID 
    # were already looped over. if so, will delete position in list and update with appropriate path. if it doesn't find a session ID, it
    # just attempts to find if the subject has already been looped over
    if 'session' in obj['output']['meta'].keys():
        if (obj['output']['meta']['subject'] in subjects) and (obj['output']['meta']['session'] in sessions):
            index = np.where(np.logical_and(subjects == obj['output']['meta']['subject'],sessions == obj['output']['meta']['session']))
            if finish_dates[index] <= obj["finish_date"]:
                subjects = np.delete(subjects,index)
                paths = np.delete(paths,index)
                sessions = np.delete(sessions,index)
                finish_dates = np.delete(finish_dates,index)
    else:
        if (obj['output']['meta']['subject'] in subjects):
            index = np.where(subjects == obj['output']['meta']['subject'])
            if finish_dates[index] <= obj["finish_date"]:
                subjects = np.delete(subjects,index)
                paths = np.delete(paths,index)
                sessions = np.delete(sessions,index)
                finish_dates = np.delete(finish_dates,index)

    return finish_dates, subjects, sessions, paths

# this will check to see if the datatype tags or tags of the datatype object exists within the filtered ('!') tags
def check_for_filter_tags(input_tags,obj,tagOrDatatypeTag):
    
    filter_checks = 0
    for i in input_tags:
        if i.replace('!','') not in obj['output'][tagOrDatatypeTag]:
            filter_checks = filter_checks+1

    return filter_checks

## this function is the wrapper function that calls all the prevouis functions to generate a dataframe for the entire project of the appropriate datatype
def collect_data(datatype,datatype_tags,tags,filename,outPath,net_adj,project_id):

    # grab path and data objects
    objects = requests.get('https://brainlife.io/api/warehouse/secondary/list/%s'%project_id).json()

    # subjects and paths
    subjects = []
    sessions = []
    paths = []
    finish_dates = []
    obj_datatype_tags = []
    obj_tags = []

    # set up output
    data = pd.DataFrame()

    # loop through objects and find appropriate objects based on datatype, datatype_tags, and tags. can include drop tags ('!'). this logic could probably be simplified
    for obj in objects:
        if obj['datatype']['name'] == datatype:
            # if datatype_tags is set, identify data using this info. if not, just use tag data. if no tags either, just append if meets datatype criteria. will check for filter with a not tag (!)
            if datatype_tags:
                # if the input datatype_tags are included in the object's datatype_tags, look for appropriate tags. if no tags, just append
                if 'datatype_tags' in list(obj['output'].keys()) and len(obj['output']['datatype_tags']) != 0:
                    if '!' in str(datatype_tags):
                        datatype_tags_to_drop = [ f for f in datatype_tags if '!' in str(f) ]
                        datatype_tag_keep = [ f for f in datatype_tags if f not in datatype_tags_to_drop ]

                        if set(datatype_tag_keep).issubset(obj['output']['datatype_tags']):
                            datatype_tag_checks = check_for_filter_tags(datatype_tags_to_drop,obj,'datatype_tags')
                            if datatype_tag_checks == len(datatype_tags_to_drop):
                                datatype_tag_filter = True
                            else:
                                datatype_tag_filter = False
                        else:
                            datatype_tag_filter = False
                    else:
                        if set(datatype_tags).issubset(obj['output']['datatype_tags']):
                            datatype_tag_filter = True
                        else:
                            datatype_tag_filter = False
                else:
                    datatype_tag_filter = False
            else:
                datatype_tag_filter = True

            if tags:
                if 'tags' in list(obj['output'].keys()) and len(obj['output']['tags']) != 0:
                    if '!' in str(tags):
                        tags_drop = [ f for f in tags if '!' in str(f) ]
                        tags_keep = [ f for f in tags if f not in tags_drop ]

                        if set(tags_keep).issubset(obj['output']['tags']):
                            tag_checks = checkcheck_for_filter_tagsForFilterTags(tags_drop,obj,'tags')
                            if tag_checks == len(tags_drop):
                                tag_filter = True
                            else:
                                tag_filter = False
                        else:
                            tag_filter = False
                    else:
                        if set(tags).issubset(obj['output']['tags']):
                            tag_filter = True
                        else:
                            tag_filter = False
                else:
                    tag_filter = False
            else:
                tag_filter = True

            if datatype_tag_filter == True & tag_filter == True:
                obj_datatype_tags = np.append(obj_datatype_tags,obj['output']['datatype_tags'])
                obj_tags = np.append(obj_tags,obj['output']['tags'])
                finish_dates, subjects, sessions, paths = append_data(subjects,sessions,paths,finish_dates,obj,filename)

    # shuffle data so subjects are in order
    paths = [z for _,_,z in sorted(zip(subjects,sessions,paths))]
    subjects = [x for x,_,_ in sorted(zip(subjects,sessions,paths))]
    sessions = [y for _,y,_ in sorted(zip(subjects,sessions,paths))]

    # check if tab separated or comma separated by looking at input filename
    if '.tsv' in filename:
        sep = '\t'
    else:
        sep = ','

    # compile data
    if net_adj:
        data = {}
        data = compile_network_adjacency_matrices(paths,subjects,sessions,data)
        if outPath:
            np.save(outPath,data)
    else:
        data = compile_data(paths,subjects,sessions,data)

    # output data structure for records and any further analyses
    if outPath:
        data.to_csv(outPath,sep=sep,index=False)

    return data


def main():
    # load config
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	# make output directories
	if not os.path.exists('./tractmeasures'):
		os.mkdir('./tractmeasures')

    # set input values
    datatype_tags = config['datatype_tags']
    tags = config['tags']
    datatype = config['datatype']
    filename = config['filename']
    project_id = config['_inputs'][0]['project']

    net_adj = False # this is for network.json data
    outPath = './tractmeasures/tractmeasures.csv'

    # collect data
    df = collect_data(datatype,datatype_tags,tags,filename,outPath,net_adj,project_id)

