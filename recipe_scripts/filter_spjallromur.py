#-*- coding: utf-8 -*- 
########################################################################
#filter_spjallromur.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 03rd, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 filter_spjallromur.py

#Description:

#This script filters empty recordings and rcordings that are
#too long.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import os
import wave
import contextlib

########################################################################
#Important Variables

MIN_LENGTH=2.0
MAX_LENGTH=30.0

########################################################################
#Global Functions

def wav_duration(audio_in):
	with contextlib.closing(wave.open(audio_in,'r')) as audio_file:
		frames = audio_file.getnframes()
		rate = audio_file.getframerate()
		duration = frames / float(rate)
	#ENDWITH
	return duration
#ENDDEF

def get_id(path_in):
	wav_id=os.path.basename(path_in)
	wav_id=wav_id.replace(".wav","")
	return wav_id
#ENDDEF

########################################################################
#Main Function

def filter_spjallromur(list_wav_paths, hash_trans):

	#--------------------------------------------------------------#
	#Filter the wavs
	HASH_WAVS_OK={}
	for path in list_wav_paths:
		duration=wav_duration(path)
		if duration>=MIN_LENGTH and duration <= MAX_LENGTH:
			wav_id=get_id(path)
			HASH_WAVS_OK[wav_id]=path
		#ENDIF
	#ENDFOR
	
	#--------------------------------------------------------------#
	#Filter the Transcriptions
	HASH_TRANS_OK={}
	for wav_id in HASH_WAVS_OK:
		if wav_id in hash_trans:
			trans_out=hash_trans[wav_id]
			HASH_TRANS_OK[wav_id]=trans_out
		#ENDFOR
	#ENDFOR	
	return [HASH_WAVS_OK, HASH_TRANS_OK]	
#ENDDEF

########################################################################

