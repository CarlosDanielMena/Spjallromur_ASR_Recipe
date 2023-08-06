#-*- coding: utf-8 -*- 
########################################################################
#rename_spjallromur.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 02nd, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 rename_spjallromur.py

#Description:

#This is script assign shorter names to all the Spjallromur files and
#copy them to a new folder called "spjallromur_renamed".

#Notice: This program is intended for Python 3
########################################################################
#Imports

import os
import shutil
import json

########################################################################
#Important Variables

DIR_CORPUS_RENAMED="spjallromur_renamed"

NEW_DIR_DATA="speech"

NEW_DIR_HALF="half"

NEW_DIR_FULL="full"

########################################################################
#Main Function

def rename_spjallromur(path_half, path_full):

	#--------------------------------------------------------------#
	#Creating important directories
	PATH_EXTRACTED_DATA=os.path.dirname(path_half)
	path_extracted=os.path.dirname(PATH_EXTRACTED_DATA)
	PATH_CORPUS_VERSIONS=os.path.dirname(path_extracted)
	PATH_CORPUS_RENAMED=os.path.join(PATH_CORPUS_VERSIONS,DIR_CORPUS_RENAMED)
	if not os.path.exists(PATH_CORPUS_RENAMED):
		os.mkdir(PATH_CORPUS_RENAMED)
	#ENDIF
	
	path_data=os.path.join(PATH_CORPUS_RENAMED,NEW_DIR_DATA)
	if not os.path.exists(path_data):
		os.mkdir(path_data)
	#ENDIF
	
	NEW_PATH_HALF=os.path.join(path_data,NEW_DIR_HALF)
	if not os.path.exists(NEW_PATH_HALF):
		os.mkdir(NEW_PATH_HALF)
	#ENDIF
	
	NEW_PATH_FULL=os.path.join(path_data,NEW_DIR_FULL)
	if not os.path.exists(NEW_PATH_FULL):
		os.mkdir(NEW_PATH_FULL)
	#ENDIF
		
	#--------------------------------------------------------------#
	#Getting the paths to the WAV files and 
	#calculating the short IDs.

	HASH_EQUI_CLAVES={}
	HASH_OLD_PATHS={}

	for root, dirs, files in os.walk(PATH_EXTRACTED_DATA):
		for filename in files:
			path_to_file=os.path.join(root,filename)
			#_demographics.json
			#_transcript.json
			if path_to_file.endswith(".wav"):

				#Quita el salto de linea de la linea actual
				path_in = path_to_file.replace("\n","")
				audio=os.path.basename(path_in)
				clave_larga=audio.replace(".wav","")
				lista_clave_larga=clave_larga.split('_')
				clave_corta=lista_clave_larga[-1]
				lista_clave_corta=clave_corta.split('-')
				clave=lista_clave_corta[0]
				clave=clave.upper()
				
				HASH_EQUI_CLAVES[clave_larga]=clave
				HASH_OLD_PATHS[clave_larga]=path_in
			#ENDIF
		#ENDFOR
	#ENDFOR

	#--------------------------------------------------------------#
	#Find out the gender of the speakers

	HASH_GENDER={}

	for clave_larga in HASH_OLD_PATHS:
		path=HASH_OLD_PATHS[clave_larga]
		path= path.replace(".wav","_demographics.json")

		with open(path,'r') as archivo_json:
			hash_demo=json.load(archivo_json)
			if hash_demo['gender']=="karl":
				gender="M"
			elif hash_demo['gender']=="kona":
				gender="F"
			elif hash_demo['gender']=="annad":
				gender="M"
			#ENDIF
			HASH_GENDER[clave_larga]=gender
		#ENDWITH
	#ENDFOR
	#--------------------------------------------------------------#
	#Calculate new paths to copy the renamed files
	
	HASH_SPK_DIRS={}
	
	for clave_larga in HASH_OLD_PATHS:
		lista_clave=clave_larga.split("_")
		canal=lista_clave[1]
		canal=canal.upper()
		
		path=HASH_OLD_PATHS[clave_larga]
		new_dir=path.replace("spjallromur_extracted",DIR_CORPUS_RENAMED)
		new_dir=new_dir.replace("data",NEW_DIR_DATA)
		new_dir=new_dir.replace("half_conversations",NEW_DIR_HALF)
		new_dir=new_dir.replace("full_conversations",NEW_DIR_FULL)
		lista_new_dir=new_dir.split(os.sep)
		clave_larga=lista_new_dir[-1]
		clave_larga=clave_larga.replace(".wav","")
		lista_new_dir.pop(-1)
		lista_new_dir.pop(-1)
		sesion=HASH_EQUI_CLAVES[clave_larga]
		
		gender=HASH_GENDER[clave_larga]
		new_name=gender+"_"+sesion+"_"+canal
				
		lista_new_dir.append(sesion)
		new_path=(os.sep).join(lista_new_dir)
		
		if not os.path.exists(new_path):
			os.mkdir(new_path)
		#ENDIF

		new_path=os.path.join(new_path,new_name)
		
		if not os.path.exists(new_path):
			os.mkdir(new_path)
		#ENDIF
			
		HASH_SPK_DIRS[clave_larga]=new_path
	#ENDFOR
	
	#--------------------------------------------------------------#
	#Copy the files to the new paths
	
	LIST_AUDIO_PATHS=[]
	LIST_TRANS_PATHS=[]
	
	for clave_larga in HASH_OLD_PATHS:
	
		ORG_audio=HASH_OLD_PATHS[clave_larga]
		ORG_trans=ORG_audio.replace(".wav","_transcript.json")
		
		DST=HASH_SPK_DIRS[clave_larga]
		spk_dir=os.path.basename(DST)
		new_name="SPMR_"+spk_dir
		DST_audio=os.path.join(DST,new_name)
		DST_audio=DST_audio+".wav"
				
		DST_trans=os.path.join(DST,new_name)
		DST_trans=DST_trans+"_transcript.json"
		
		#Copy the audio files with a new name
		if not os.path.exists(DST_audio):
			shutil.copy(ORG_audio,DST_audio)
		#ENDIF
		
		#Copy the transcription files with a new name
		if not os.path.exists(DST_trans):
			shutil.copy(ORG_trans,DST_trans)
		#ENDIF
		LIST_AUDIO_PATHS.append(DST_audio)
		LIST_TRANS_PATHS.append(DST_trans)
	#ENDFOR
	
	return [LIST_AUDIO_PATHS, LIST_TRANS_PATHS]
#ENDDEF

########################################################################

