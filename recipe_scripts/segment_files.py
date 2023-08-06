#-*- coding: utf-8 -*- 
########################################################################
#segment_files.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 02nd, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 segment_files.py

#Description:

#This script creates the segment files ".segments" which contain 
#just the transcripts with timestamps in a plain text format. The 
#segment files are generated in the same folder as the renamed json 
#files.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import re
import os
import json

########################################################################

def redondea_tiempo(time_in):
	if time_in==None:
		time_in="0.0s"
	#ENDIF

	time_out=time_in.replace("s","")
	time_out=float(time_out)
	time_out=round(time_out,3)
	time_out=str(time_out)
	return time_out
#ENDDEF

########################################################################

def segment_files(list_audio_paths):

	LIST_SEGMENT_PATHS=[]
	for path in list_audio_paths:
		#Quita el salto de linea de la linea actual
		path = path.replace("\n","")
		
		path_out=path.replace("_transcript.json",".segments")
		
		LIST_SEGMENT_PATHS.append(path_out)
		
		#Abre el archivo de salida
		archivo_out=open(path_out,'w')
		
		#Abre el archivo de entrada
		archivo_json = open(path,'r')
		
		#Carga el archivo en un objeto de python
		HASH_JSON=json.load(archivo_json)

		for hash_segment in HASH_JSON["segments"]:

			start_time=hash_segment['startTime']
			end_time=hash_segment['endTime']
			
			linea=""
			for hash_words in hash_segment["words"]:
				linea=linea+" "+hash_words["word"]
			#ENDFOR
			linea=linea.replace("."," ")
			linea=linea.replace(","," ")
			linea=linea.replace("?"," ")
			linea=re.sub('\s+',' ',linea)
			linea=linea.strip()
			linea=linea.lower()
			
			#print(path)
			start_time=redondea_tiempo(start_time)
			end_time=redondea_tiempo(end_time)
				
			linea_out=start_time+" "+end_time+" "+linea
			archivo_out.write(linea_out+"\n")
		#ENDFOR
		
		#Cierra los archivos abiertos
		archivo_json.close()
		archivo_out.close()
	#ENDFOR
	
	return LIST_SEGMENT_PATHS
#ENDDEF

########################################################################

