#-*- coding: utf-8 -*- 
########################################################################
#run_recipe.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 01st, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 run_recipe.py

#Description:

#This is scripts runs all the scripts that are necessary to perform
#an ASR experiment using the corpus Spjallromur and the Speech
#Recognition system Whisper.

#You can see more information about Spjallromur at:
#http://hdl.handle.net/20.500.12537/187

#Notice: This program is intended for Python 3
########################################################################
#Presentation

print("---------------------------------------------------------")
print("              Spjallromur ASR Recipe")
print("                       by")
print("Language and Voice Laboratory of Reykjavík University")
print("---------------------------------------------------------")
print("\n")

########################################################################
#Donwload Spjallromur

from recipe_scripts.download_spjallromur import download_spjallromur
print("(01 of 10) Donwloading Spjallromur ...")
PATH_ZIP_HALF, PATH_ZIP_FULL = download_spjallromur()

########################################################################
#Extract Spjallromur

from recipe_scripts.extract_spjallromur import extract_spjallromur
print("(02 of 10) Extracting Spjallromur ...")
PATH_HALF, PATH_FULL , PATH_README=extract_spjallromur(PATH_ZIP_HALF, PATH_ZIP_FULL)

########################################################################
#Rename Spjallromur
from recipe_scripts.rename_spjallromur import rename_spjallromur
print("(03 of 10) Renaming Spjallromur Files ...")
LIST_AUDIO_PATHS, LIST_TRANS_PATHS=rename_spjallromur(PATH_HALF,PATH_FULL)

########################################################################
#Creating the segment files which contain just the transcripts with
#timestamps in a plain text format.
from recipe_scripts.segment_files import segment_files
print("(04 of 10) Creating Segment Files \".segments\" ...")
LIST_SEGMENT_PATHS=segment_files(LIST_TRANS_PATHS)

########################################################################
#Segment Spjallromur
from recipe_scripts.segment_spjallromur import segment_spjallromur
print("(05 of 10) Segmenting Spjallromur ...")
LIST_WAV_PATHS, HASH_TRANS, PATH_CORPUS_VERSIONS=segment_spjallromur(LIST_SEGMENT_PATHS)

########################################################################
#Filter Spjallromur
from recipe_scripts.filter_spjallromur import filter_spjallromur
print("(06 of 10) Filtering Spjallromur ...")
HASH_WAVS_OK, HASH_TRANS_OK=filter_spjallromur(LIST_WAV_PATHS,HASH_TRANS)

########################################################################
#Generate the ASR corpus "spjallromur_asr"
from recipe_scripts.spjallromur_asr import spjallromur_asr
print("(07 of 10) Generating spjallromur_asr ...")
PATH_SPJALLROMUR_FILES=spjallromur_asr(HASH_WAVS_OK,HASH_TRANS_OK,PATH_CORPUS_VERSIONS,PATH_README)

########################################################################
#Download the ASR model "language-and-voice-lab/whisper-large-icelandic-30k-steps-1000h-ct2"
from recipe_scripts.download_asr_model import download_asr_model
print("(08 of 10) Downloading the ASR model from Hugging Face ...")
PATH_ASR_MODEL=download_asr_model()
########################################################################
#Transcribe the Dev and Test splits using Faster-Whisper
from recipe_scripts.transcribe_splits import transcribe_splits
print("(09 of 10) Transcribing the Dev and Test splits using Faster-Whisper ...")
PATH_HYP_TEST_TRANS, PATH_HYP_DEV_TRANS=transcribe_splits(PATH_SPJALLROMUR_FILES,PATH_ASR_MODEL)

########################################################################
#Calculate the WER of Dev and Test splits using jiwer
from recipe_scripts.calculate_wer import calculate_wer
print("(10 of 10) Calculating WER of the Dev and Test splits ...")
calculate_wer(PATH_SPJALLROMUR_FILES,PATH_HYP_TEST_TRANS,PATH_HYP_DEV_TRANS)

########################################################################
print("\n")
print("---------------------------------------------------------")
print("           Recipe Successfully Executed!!!")
print("---------------------------------------------------------")

########################################################################

