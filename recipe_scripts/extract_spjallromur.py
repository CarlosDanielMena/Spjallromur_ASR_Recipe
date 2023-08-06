#-*- coding: utf-8 -*- 
########################################################################
#template_ENG_python3.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 01st, 2023
#Location : Reykjavík University
#Location : Garðastræti 6, 101 Reykjavík

#Usage:

#	$ python3 template_ENG_python3.py <file_in>

#Example:

#	$ python3 template_ENG_python3.py file_in.txt

#Description:

#This script is destined to extract Spjallromur in the same
#directory it was downloaded.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import os
import shutil
import zipfile

########################################################################
#Important Variables

DIR_CORPUS_EXTRACTED="spjallromur_extracted"

PARTIAL_PATH_HALF=os.path.join("spjallromur","data","half_conversations")

PARTIAL_PATH_FULL=os.path.join("spjallromur","data","full_conversations")

PARTIAL_PATH_README=os.path.join("spjallromur","docs","spjallromur_README.txt")

NAME_README_ORG="spjallromur_README.txt"

DIR_CORPUS_DATA="data"

DIR_CORPUS_DOCS="docs"

########################################################################
#Main Function

def extract_spjallromur(path_half_zip,path_full_zip):

	#Getting the path of the extraction directory
	list_path=path_half_zip.split(os.sep)
	list_path.pop(-1)
	list_path.pop(-1)
	PATH_CORPUS_VERSIONS=(os.sep).join(list_path)
	PATH_CORPUS_EXTRACTED=os.path.join(PATH_CORPUS_VERSIONS,DIR_CORPUS_EXTRACTED)
		
	#Creating the extraction directory
	if not os.path.exists(PATH_CORPUS_EXTRACTED):
		os.mkdir(PATH_CORPUS_EXTRACTED)
	#ENDIF	

	#Verify that the zip files exist.
	error=False
	if not os.path.exists(path_half_zip):
		print("ERROR: File "+path_half_zip+" does not exist!")
		error=True
	#ENDIF
	
	if not os.path.exists(path_full_zip):
		print("ERROR: File "+path_full_zip+" does not exist!")
		error=True
	#ENDIF
	
	if error==True:
		exit()
	#ENDIF

	extraction_dir=PATH_CORPUS_EXTRACTED
	storage_dir=os.path.join(extraction_dir,DIR_CORPUS_DATA)
	
	if not os.path.exists(storage_dir):
		os.mkdir(storage_dir)
	#ENDIF
	
	#Extracting the half conversations
	
	#Avoid errors caused by an incomplete extraction
	spjallromur_dir=os.path.join(extraction_dir,"spjallromur")
	if os.path.exists(spjallromur_dir):
		shutil.rmtree(spjallromur_dir)
	#ENDIF
	
	storage_half_dir=os.path.join(storage_dir,"half_conversations")
	move_half_dir=os.path.join(extraction_dir,PARTIAL_PATH_HALF)
	
	if not os.path.exists(storage_half_dir):
		#Extracting half conversations
		with zipfile.ZipFile(path_half_zip, 'r') as zip_ref:
			zip_ref.extractall(extraction_dir)
		#ENDWITH
		shutil.move(move_half_dir,storage_dir)
		shutil.rmtree(spjallromur_dir)
	#ENDIF
	
	#Extracting the full conversations		
	
	#Avoid errores caused by an incomplete extraction
	spjallromur_dir=os.path.join(extraction_dir,"spjallromur")
	if os.path.exists(spjallromur_dir):
		shutil.rmtree(spjallromur_dir)
	#ENDIF
	
	storage_full_dir=os.path.join(storage_dir,"full_conversations")
	move_full_dir=os.path.join(extraction_dir,PARTIAL_PATH_FULL)
	if not os.path.exists(storage_full_dir):
		#Extracting full conversations
		with zipfile.ZipFile(path_full_zip, 'r') as zip_ref:
			zip_ref.extractall(extraction_dir)
		#ENDWITH
		shutil.move(move_full_dir,storage_dir)
		
		docs_dir=os.path.join(extraction_dir,DIR_CORPUS_DOCS)
		if not os.path.exists(docs_dir):
			os.mkdir(docs_dir)
		#ENDIF
		readme_path=os.path.join(extraction_dir,PARTIAL_PATH_README)
		shutil.move(readme_path,docs_dir)
		
		shutil.rmtree(spjallromur_dir)
	#ENDIF
	new_readme_path=os.path.join(PATH_CORPUS_EXTRACTED,DIR_CORPUS_DOCS,NAME_README_ORG)
	return [storage_half_dir,storage_full_dir,new_readme_path]
#ENDDEF

########################################################################

