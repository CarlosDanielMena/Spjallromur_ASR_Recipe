#-*- coding: utf-8 -*- 
########################################################################
#download_spjallromur.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 01st, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 download_spjallromur.py

#Example:

#	$ python3 download_spjallromur.py

#Description:

#This is script downloads the Spjallrmur corpus from Clarin.is
#See: http://hdl.handle.net/20.500.12537/187

#Notice: This program is intended for Python 3
########################################################################
#Imports

import os
import requests

########################################################################
#Important paths

CURRENT_PATH=os.getcwd()
DIR_CORPUS_VERSIONS="corpus_versions"
PATH_CORPUS_VERSIONS=os.path.join(CURRENT_PATH,DIR_CORPUS_VERSIONS)

DIR_SPJALLROMUR="spjallromur_downloaded"
PATH_SPJALLROMUR=os.path.join(PATH_CORPUS_VERSIONS,DIR_SPJALLROMUR)

ZIP_HALF_CONVERSATIONS="spjallromur_half_conversations.zip"
PATH_HALF=os.path.join(PATH_SPJALLROMUR,ZIP_HALF_CONVERSATIONS)

ZIP_FULL_CONVERSATIONS="spjallromur_full_conversations.zip"
PATH_FULL=os.path.join(PATH_SPJALLROMUR,ZIP_FULL_CONVERSATIONS)

CORPUS_URL="https://repository.clarin.is/repository/xmlui/bitstream/handle/20.500.12537/187"
URL_HALF=os.path.join(CORPUS_URL,ZIP_HALF_CONVERSATIONS)
URL_FULL=os.path.join(CORPUS_URL,ZIP_FULL_CONVERSATIONS)

########################################################################
#Main function

def download_spjallromur():

	#Create a folder for the different versions of the corpus
	if not os.path.exists(PATH_CORPUS_VERSIONS):
		os.mkdir(PATH_CORPUS_VERSIONS)
	#ENDIF
	
	#Create a folder for Spjallromur
	if not os.path.exists(PATH_SPJALLROMUR):
		os.mkdir(PATH_SPJALLROMUR)
	#ENDIF
	
	#Download half conversations
	if not os.path.exists(PATH_HALF):
		None
		# URL of the corpus to be downloaded is defined as URL_HALF
		r = requests.get(URL_HALF) # create HTTP response object
		
		# send a HTTP request to the server and save
		# the HTTP response in a response object called r
		with open(PATH_HALF,'wb') as f:
		  
			# Saving received content as a zip file in
			# binary format

			# write the contents of the response (r.content)
			# to a new file in binary mode.
			f.write(r.content)
		#ENDWITH
	#ENDIF
	
	#Download full conversations
	if not os.path.exists(PATH_FULL):
		None
		# URL of the corpus to be downloaded is defined as URL_FULL
		r = requests.get(URL_FULL) # create HTTP response object
		
		# send a HTTP request to the server and save
		# the HTTP response in a response object called r
		with open(PATH_FULL,'wb') as f:
		  
			# Saving received content as a zip file in
			# binary format

			# write the contents of the response (r.content)
			# to a new file in binary mode.
			f.write(r.content)
		#ENDWITH
	#ENDIF
	
	return [PATH_HALF,PATH_FULL]
#ENDDEF

########################################################################

