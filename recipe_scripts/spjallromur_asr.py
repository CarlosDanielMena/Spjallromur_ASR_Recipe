#-*- coding: utf-8 -*- 
########################################################################
#spjallromur_asr.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 03rd, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 spjallromur_asr.py

#Description:

#This script generates the final transformation of the corpus
#Spjallromur called "spjallromur_asr".

#Notice: This program is intended for Python 3
########################################################################
#Imports

import os
import shutil

########################################################################
#Important Variables

DIR_CORPUS_ASR="spjallromur_asr"

DIR_RECIPE_SCRIPTS="recipe_scripts"

FILE_TRAIN_SPLIT="spjallromur_train.split"

FILE_TEST_SPLIT="spjallromur_test.split"

FILE_DEV_SPLIT="spjallromur_dev.split"

NAME_NEW_README="README.txt"

DIR_CORPUS_DATA="speech"

DIR_CORPUS_DOCS="files"

NAME_TRAIN="SPJALLROMUR_TRAIN"

NAME_TEST="SPJALLROMUR_TEST"

NAME_DEV="SPJALLROMUR_DEV"

########################################################################
#Global Functions

def read_split_file(path_split_file):
	HASH_SPLIT={}
	LIST_IDS=[]
	file_current_split=open(path_split_file,'r')
	for path in file_current_split:
		path=path.replace('\n','')
		wav_id=os.path.basename(path)
		HASH_SPLIT[wav_id]=path
		LIST_IDS.append(wav_id)
	#ENDFOR
	LIST_IDS.sort()
	file_current_split.close()
	return [HASH_SPLIT,LIST_IDS]
#ENDDEF

def create_trans_file(path_trans_file,hash_trans,list_ids):
	file_current_trans=open(path_trans_file,'w')
	for wav_id in list_ids:
		if wav_id in hash_trans:
			trans_out=hash_trans[wav_id]
			file_current_trans.write(trans_out+"\n")
		#ENDIF
	#ENDFOR
	file_current_trans.close()
#ENDDEF

def create_dir_tree(path_split_file,path_root_dir):
	#Read the split file
	HASH_FOLDERS={}
	HASH_NEW_PATHS={}
	file_current_split=open(path_split_file,'r')
	for path in file_current_split:
		path=path.replace('\n','')
		list_path=path.split('/')
		list_path.pop(0)
		list_path.pop(-1)
		
		acumm=""
		for item in list_path:
			acumm=os.path.join(acumm,item)
			HASH_FOLDERS[acumm]=len(acumm)
		#ENDFOR
	#ENDFOR
	file_current_split.close()

	#Determine the correct order of creation of the folders
	LIST_TUPLES=[]
	for path in HASH_FOLDERS:
		longi=HASH_FOLDERS[path]
		LIST_TUPLES.append([longi,path])
	#ENDFOR
	LIST_TUPLES.sort()
	
	#Create the directory tree
	for longi,path in LIST_TUPLES:
		path_folder=os.path.join(path_root_dir,path)
		if not os.path.exists(path_folder):
			os.mkdir(path_folder)
		#ENDIF
	#ENDFOR
#ENDDEF

def calc_new_paths(path_split_file,path_root_dir):
	HASH_NEW_PATHS={}
	file_current_split=open(path_split_file,'r')
	for path in file_current_split:
		path=path.replace('\n','')
		list_path=path.split('/')
		list_path.pop(0)
		path_tail=(os.sep).join(list_path)
		wav_id=os.path.basename(path_tail)
		NEW_PATH=os.path.join(path_root_dir,path_tail)
		NEW_PATH=NEW_PATH+".wav"
		HASH_NEW_PATHS[wav_id]=NEW_PATH
	#ENDFOR
	return HASH_NEW_PATHS
#ENDDEF

def copy_audios(hash_org,hash_dst):
	for wav_id in hash_dst:
		ORG=hash_org[wav_id]
		DST=hash_dst[wav_id]
		#Copy the audio files
		if not os.path.exists(DST):
			shutil.copy(ORG,DST)
		#ENDIF
	#ENDDEF
#ENDDEF

def create_paths_file(path_wav_paths,hash_wav_paths):
	file_current_paths=open(path_wav_paths,'w')
	LIST_WAV_PATHS=list(hash_wav_paths.items())
	LIST_WAV_PATHS.sort()
	for wav_id,path in LIST_WAV_PATHS:
		file_current_paths.write(path+"\n")
	#ENDFOR
	file_current_paths.close()
#ENDDEF

########################################################################
#Main Function

def spjallromur_asr(HASH_WAVS_OK,HASH_TRANS_OK,PATH_CORPUS_VERSIONS,PATH_README):
	#--------------------------------------------------------------#
	#Create the directory tree for "spjallromur_asr"
	PATH_CORPUS_ASR=os.path.join(PATH_CORPUS_VERSIONS,DIR_CORPUS_ASR)
	if not os.path.exists(PATH_CORPUS_ASR):
		os.mkdir(PATH_CORPUS_ASR)
	#ENDIF
	#--------------------------------------------------------------#
	#Copy the README file to "spjallromur_asr"
	PATH_NEW_README=os.path.join(PATH_CORPUS_ASR,NAME_NEW_README)
	shutil.copy(PATH_README,PATH_NEW_README) 
	#--------------------------------------------------------------#
	#Create the main folders of "spjallromur_asr"
	PATH_CORPUS_DATA=os.path.join(PATH_CORPUS_ASR,DIR_CORPUS_DATA)
	if not os.path.exists(PATH_CORPUS_DATA):
		os.mkdir(PATH_CORPUS_DATA)
	#ENDIF
	PATH_CORPUS_DOCS=os.path.join(PATH_CORPUS_ASR,DIR_CORPUS_DOCS)
	if not os.path.exists(PATH_CORPUS_DOCS):
		os.mkdir(PATH_CORPUS_DOCS)
	#ENDIF
	#--------------------------------------------------------------#
	#Calculate paths to the files with the corpus splits
	PATH_TRAIN_SPLIT=os.path.join(DIR_RECIPE_SCRIPTS,FILE_TRAIN_SPLIT)
	PATH_TEST_SPLIT=os.path.join(DIR_RECIPE_SCRIPTS,FILE_TEST_SPLIT)
	PATH_DEV_SPLIT=os.path.join(DIR_RECIPE_SCRIPTS,FILE_DEV_SPLIT)
	#--------------------------------------------------------------#
	#Read the split files
	HASH_TRAIN_SPLIT, LIST_TRAIN_IDS = read_split_file(PATH_TRAIN_SPLIT)
	HASH_TEST_SPLIT, LIST_TEST_IDS = read_split_file(PATH_TEST_SPLIT)
	HASH_DEV_SPLIT, LIST_DEV_IDS = read_split_file(PATH_DEV_SPLIT)
	#--------------------------------------------------------------#	
	#Calculate the paths to the transcription files per split
	PATH_TRAIN_TRANS=os.path.join(PATH_CORPUS_DOCS,NAME_TRAIN+".trans")
	PATH_TEST_TRANS=os.path.join(PATH_CORPUS_DOCS,NAME_TEST+".trans")
	PATH_DEV_TRANS=os.path.join(PATH_CORPUS_DOCS,NAME_DEV+".trans")	
	#--------------------------------------------------------------#	
	#Create the transcription files per split
	create_trans_file(PATH_TRAIN_TRANS,HASH_TRANS_OK,LIST_TRAIN_IDS)
	create_trans_file(PATH_TEST_TRANS,HASH_TRANS_OK,LIST_TEST_IDS)
	create_trans_file(PATH_DEV_TRANS,HASH_TRANS_OK,LIST_DEV_IDS)
	#--------------------------------------------------------------#	
	#Create the directory tree for each split
	create_dir_tree(PATH_TRAIN_SPLIT,PATH_CORPUS_DATA)
	create_dir_tree(PATH_TEST_SPLIT,PATH_CORPUS_DATA)
	create_dir_tree(PATH_DEV_SPLIT,PATH_CORPUS_DATA)
	#--------------------------------------------------------------#	
	#Calculate new paths for each audio file
	HASH_TRAIN_DST=calc_new_paths(PATH_TRAIN_SPLIT,PATH_CORPUS_DATA)
	HASH_TEST_DST=calc_new_paths(PATH_TEST_SPLIT,PATH_CORPUS_DATA)
	HASH_DEV_DST=calc_new_paths(PATH_DEV_SPLIT,PATH_CORPUS_DATA)
	#--------------------------------------------------------------#	
	#Copy the audio files to "spjallromur_asr"
	copy_audios(HASH_WAVS_OK,HASH_TRAIN_DST)
	copy_audios(HASH_WAVS_OK,HASH_TEST_DST)
	copy_audios(HASH_WAVS_OK,HASH_DEV_DST)
	#--------------------------------------------------------------#
	#Calculate the paths to the path files per split
	PATH_TRAIN_PATHS=os.path.join(PATH_CORPUS_DOCS,NAME_TRAIN+".paths")
	PATH_TEST_PATHS=os.path.join(PATH_CORPUS_DOCS,NAME_TEST+".paths")
	PATH_DEV_PATHS=os.path.join(PATH_CORPUS_DOCS,NAME_DEV+".paths")
	#--------------------------------------------------------------#	
	#Create the path files per split
	create_paths_file(PATH_TRAIN_PATHS,HASH_TRAIN_DST)
	create_paths_file(PATH_TEST_PATHS,HASH_TEST_DST)
	create_paths_file(PATH_DEV_PATHS,HASH_DEV_DST)	
	#--------------------------------------------------------------#
	return PATH_CORPUS_DOCS
#ENDDEF

########################################################################

