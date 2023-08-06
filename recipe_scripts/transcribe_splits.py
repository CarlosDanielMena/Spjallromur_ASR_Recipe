#-*- coding: utf-8 -*- 
########################################################################
#transcribe_splits.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 05th, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 transcribe_splits.py

#Description:

#This script transcribe the Dev and Test portions using the
#model of Faster-Whisper previously downloaded.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import re
import os
from faster_whisper import WhisperModel

########################################################################
#Important Variables

FILE_TEST_PATHS="SPJALLROMUR_TEST.paths"

FILE_DEV_PATHS="SPJALLROMUR_DEV.paths"

DIR_RES_TRANS="resulting_transcriptions"

FILE_OUT_TEST_TRANS="RESULTING_TEST.trans"

FILE_OUT_DEV_TRANS="RESULTING_DEV.trans"

FASTER_WHISPER_MODEL = "whisper-large-icelandic-30k-steps-1000h-ct2"

########################################################################
#Whisper Fast Configuration

#You can choose to transcribe using either CPU or GPU depending
#on you system. The default option is CPU. 

#Just uncomment your desired option.

def whisper_fast_model_conf():

	# Run on GPU with FP16
	#model = WhisperModel(FASTER_WHISPER_MODEL, device="cuda", compute_type="float16")
	# or run on GPU with INT8
	#model = WhisperModel(FASTER_WHISPER_MODEL, device="cuda", compute_type="int8_float16")
	# or run on CPU with INT8
	model = WhisperModel(FASTER_WHISPER_MODEL, device="cpu", compute_type="int8")

	return model
#ENDDEF

########################################################################
#Global Functions

def transcribe(path_wav_paths,path_file_out):

	#Get the model
	model=whisper_fast_model_conf()
	
	file_out=open(path_file_out,'w')
	file_in=open(path_wav_paths,'r')
	#Transcribe the data
	for wav_path in file_in:
		wav_path=wav_path.replace('\n','')
		wav_id=os.path.basename(wav_path)
		wav_id=wav_id.replace('.wav','')
				
		segments, info = model.transcribe(wav_path, beam_size=5)
		
		for segment in segments:
			trans_out=segment.text
			line_out=wav_id+" "+trans_out
			line_out=re.sub('\s+',' ',line_out)
			line_out=line_out.strip()
			file_out.write(line_out+"\n")
		#ENDFOR
	#ENDFOR
	file_in.close()
	file_out.close()
#ENDDEF

########################################################################
#Main Function

def transcribe_splits(PATH_SPJALLROMUR_FILES,PATH_ASR_MODEL):
	#--------------------------------------------------------------#
	#Create the output directory for the resulting trancriptions
	CURRENT_PATH=os.getcwd()
	PATH_RES_TRANS=os.path.join(CURRENT_PATH,DIR_RES_TRANS)
	if not os.path.exists(PATH_RES_TRANS):
		os.mkdir(PATH_RES_TRANS)
	#ENDIF
	#--------------------------------------------------------------#
	#Calculating important paths
	PATH_TEST_PATHS=os.path.join(PATH_SPJALLROMUR_FILES,FILE_TEST_PATHS)
	PATH_DEV_PATHS=os.path.join(PATH_SPJALLROMUR_FILES,FILE_DEV_PATHS)

	PATH_OUT_TEST_TRANS=os.path.join(PATH_RES_TRANS,FILE_OUT_TEST_TRANS)
	PATH_OUT_DEV_TRANS=os.path.join(PATH_RES_TRANS,FILE_OUT_DEV_TRANS)
	#--------------------------------------------------------------#
	#Transcribing the Test portion
	if not os.path.exists(PATH_OUT_TEST_TRANS):
		print("\tTranscribing the Test split ...")
		transcribe(PATH_TEST_PATHS,PATH_OUT_TEST_TRANS)
	#ENDIF
	#--------------------------------------------------------------#
	#Transcribing the Dev portion
	if not os.path.exists(PATH_OUT_DEV_TRANS):
		print("\tTranscribing the Dev split ...")
		transcribe(PATH_DEV_PATHS,PATH_OUT_DEV_TRANS)
	#ENDIF
	return [PATH_OUT_TEST_TRANS, PATH_OUT_DEV_TRANS]
#ENDDEF

########################################################################

