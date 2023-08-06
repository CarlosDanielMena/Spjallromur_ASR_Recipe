#-*- coding: utf-8 -*- 
########################################################################
#segment_spjallromur.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 02nd, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 segment_spjallromur.py

#Description:

#This is a python3 template.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################
#Important Variables

DIR_CORPUS_RENAMED="spjallromur_renamed"

DIR_CORPUS_SEGMENTED="spjallromur_segmented"

NAME_FILE_TRANS="SPJALLROMUR_TRANSCRIPTIONS.trans"

########################################################################
#Global Functions

def num_format(num_in):
	MAX_LEN=5
	num_out=str(num_in)
	longi=len(num_out)
	num_zeros=MAX_LEN-longi
	num_out="0"*num_zeros+num_out
	return num_out
#ENDDEF

def numeracion(num_in):

	if num_in < 10:
		num_out = "0"+str(num_in)
	else:
		num_out = str(num_in)
	#ENDIF
	return num_out
#ENDDEF

def time_format(time_in):

	horas_totales=int(time_in / 3600)
	minutos_totales = int(time_in / 60)
	#segundos = int(time_in) - (minutos_totales * 60)
	segundos = round(time_in - (minutos_totales * 60.0),3)
	minutos = minutos_totales - (horas_totales * 60)
	
	time_out=numeracion(horas_totales)+":"+numeracion(minutos)+":"+numeracion(segundos)
	
	return time_out

#ENDDEF

def copy_dir_tree(path_dir_org, path_dir_dst):
	for root, dirs, files in os.walk(path_dir_org):
		for directory in dirs:
			path_org=os.path.join(root,directory)
			path_dst=path_org.replace(DIR_CORPUS_RENAMED,DIR_CORPUS_SEGMENTED)
			
			if not os.path.exists(path_dst):
				os.mkdir(path_dst)
			#ENDIF	
		#ENDFOR
	#ENDFOR
#ENDDEF

########################################################################
#Main Function

def segment_spjallromur(list_segment_paths):

	#--------------------------------------------------------------#
	#Creating the directory "spjallromur_segmented"
	path_org=list_segment_paths[0]
	lista_org=path_org.split(DIR_CORPUS_RENAMED)
	
	PATH_CORPUS_VERSIONS=lista_org[0]
	
	PATH_CORPUS_RENAMED=os.path.join(PATH_CORPUS_VERSIONS,DIR_CORPUS_RENAMED)
	PATH_CORPUS_SEGMENTED=os.path.join(PATH_CORPUS_VERSIONS,DIR_CORPUS_SEGMENTED)
	
	#Create the folder 
	if not os.path.exists(PATH_CORPUS_SEGMENTED):
		os.mkdir(PATH_CORPUS_SEGMENTED)
	#ENDIF
	
	#Copy the tree directory of "spjallromur_renamed" to "spjallromur_segmented"
	copy_dir_tree(PATH_CORPUS_RENAMED,PATH_CORPUS_SEGMENTED)
	
	#--------------------------------------------------------------#
	#Creates the resulting transcription file at the right path
	PATH_FILE_TRANS=os.path.join(PATH_CORPUS_SEGMENTED,NAME_FILE_TRANS)
	archivo_out=open(PATH_FILE_TRANS,'w')
	#--------------------------------------------------------------#
	#Segments the corpus
	LIST_WAV_PATHS=[]
	HASH_TRANS={}
	for path in list_segment_paths:
		NAME=os.path.basename(path)
		NAME=NAME.replace(".segments","")
				
		ORG=path.replace(".segments",".wav")
		dst=ORG.replace(DIR_CORPUS_RENAMED,DIR_CORPUS_SEGMENTED)
		dst=dst.replace(".wav","")

		archivo_actual=open(path,'r')

		CONT=0
		for linea in archivo_actual:
			linea=linea.replace("\n","")
			lista_linea=linea.split(" ")
			INI=float(lista_linea[0])
			FIN=float(lista_linea[1])
			LEN=round(FIN-INI,3)
			
			if LEN >= 2.0:
				CONT=CONT+1
				
				lista_linea.pop(0)
				lista_linea.pop(0)
				TRANS=" ".join(lista_linea)

				cont=num_format(CONT)
				INI=time_format(INI)
				LEN=time_format(LEN)
				
				DST=dst+"_"+cont+".wav"
				linea_out=NAME+"_"+cont+" "+TRANS
				
				HASH_TRANS[NAME+"_"+cont]=linea_out
				
				archivo_out.write(linea_out+"\n")
				
				if not os.path.exists(DST):
					comando="ffmpeg -loglevel panic -ss "+INI+" -t "+LEN+" -i "+ ORG +" "+DST
					#print(comando)
					os.system(comando)
					
				#ENDIF
				LIST_WAV_PATHS.append(DST)
			#ENDIF
			
		#ENDFOR
		archivo_actual.close()
	#ENDFOR
	return [LIST_WAV_PATHS, HASH_TRANS, PATH_CORPUS_VERSIONS]
#ENDDEF

########################################################################

