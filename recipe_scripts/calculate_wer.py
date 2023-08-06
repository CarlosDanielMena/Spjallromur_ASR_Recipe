#-*- coding: utf-8 -*- 
########################################################################
#calculate_wer.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 05th, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 calculate_wer.py

#Description:

#This is script calculates the Word Error Rate (WER) of the Test
#and Dev portions of the corpus "spjallromur_asr".

#Notice: This program is intended for Python 3
########################################################################
#Imports

import re
import os
import jiwer

########################################################################
#Important Variables

FILE_REF_TEST_TRANS="SPJALLROMUR_TEST.trans"

FILE_REF_DEV_TRANS="SPJALLROMUR_DEV.trans"

FILE_RESULTS="RESULTS.txt"

########################################################################
#Global Functions

def read_trans_file(path_file_trans):
	HASH_TRANS={}
	file_trans=open(path_file_trans,'r')
	for line in file_trans:
		line=line.replace('\n','')
		line=re.sub('\s+',' ',line)
		line=line.strip()
		list_line=line.split(" ")
		wav_id=list_line[0]
		list_line.pop(0)
		trans=" ".join(list_line)
		HASH_TRANS[wav_id]=trans
	#ENDFOR
	file_trans.close()
	return HASH_TRANS
#ENDDEF

def jiwer_wer(file_ref_trans,file_hyp_trans):
	#--------------------------------------------------------------#
	#Reading the input files
	HASH_REF=read_trans_file(file_ref_trans)
	HASH_HYP=read_trans_file(file_hyp_trans)
	#--------------------------------------------------------------#
	#Align transcriptions
	LIST_REF=[]
	LIST_HYP=[]
	for wav_id in HASH_HYP:
		if wav_id in HASH_REF:
			trans_ref=HASH_REF[wav_id]
			LIST_REF.append(trans_ref)
			trans_hyp=HASH_HYP[wav_id]
			LIST_HYP.append(trans_hyp)
		#ENDIF
	#ENDFOR
	#--------------------------------------------------------------#
	#Calculate the WER using jiwer
	WER=jiwer.wer(LIST_REF,LIST_HYP)
	WER=WER*100.0
	WER=round(WER,3)
	#--------------------------------------------------------------#
	return [str(WER), str(len(HASH_REF)), str(len(LIST_HYP))]
#ENDDEF

########################################################################
#Main Function

def calculate_wer(PATH_SPJALLROMUR_FILES,PATH_HYP_TEST_TRANS,PATH_HYP_DEV_TRANS):
	#--------------------------------------------------------------#
	#Calculating important paths
	PATH_REF_TEST_TRANS= os.path.join(PATH_SPJALLROMUR_FILES,FILE_REF_TEST_TRANS)
	PATH_REF_DEV_TRANS= os.path.join(PATH_SPJALLROMUR_FILES,FILE_REF_DEV_TRANS)
	#--------------------------------------------------------------#
	#Calculating the WER	
	TEST_WER, LEN_TEST_REF, LEN_TEST_HYP=jiwer_wer(PATH_REF_TEST_TRANS, PATH_HYP_TEST_TRANS)
	DEV_WER, LEN_DEV_REF, LEN_DEV_HYP =jiwer_wer(PATH_REF_DEV_TRANS, PATH_HYP_DEV_TRANS)
	#--------------------------------------------------------------#
	#Creating the RESULTS file
	CURRENT_PATH=os.getcwd()
	PATH_RESULTS=os.path.join(CURRENT_PATH,FILE_RESULTS)
	file_results=open(PATH_RESULTS,'w')

	LINE_RES_TEST="WER (Test): "+TEST_WER+"% "+" [ "+LEN_TEST_HYP +" hyp / "+LEN_TEST_REF+" ref ]" + " "+PATH_HYP_TEST_TRANS
	LINE_RES_DEV="WER (Dev) : "+DEV_WER+"% "+" [ "+LEN_DEV_HYP +" hyp / "+LEN_DEV_REF+" ref ]" + " "+PATH_HYP_DEV_TRANS
	
	file_results.write(LINE_RES_TEST+"\n")
	file_results.write(LINE_RES_DEV+"\n")

	file_results.close()
	#--------------------------------------------------------------#
	#Printing WERs in terminal
	LINE_RES_TEST="\tWER (Test): "+TEST_WER+"% "+" [ "+LEN_TEST_HYP +" hyp / "+LEN_TEST_REF+" ref ]"
	LINE_RES_DEV="\tWER (Dev) : "+DEV_WER+"% "+" [ "+LEN_DEV_HYP +" hyp / "+LEN_DEV_REF+" ref ]"
	
	print(LINE_RES_TEST)
	print(LINE_RES_DEV)
#ENDDEF

########################################################################

