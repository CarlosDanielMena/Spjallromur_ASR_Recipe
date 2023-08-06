#-*- coding: utf-8 -*- 
########################################################################
#check_dependencies.py

#Author   : Carlos Daniel Hernández Mena
#Date     : August 05th, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 check_dependencies.py

#Description:

#This scripts tries to import all the python libraries needed to
#run the recipe. It also checks the existance of ffmpeg in the system.

#If you see no error messages after running this script, then you
#will be able to successfully run the recipe in the current system.

#Notice: This program is intended for Python 3

########################################################################
#Important Variables

ERROR_FLAG=False

########################################################################
#Imports

import sys
import re
import os
import requests
import shutil
import zipfile
import wave
import contextlib
import json

########################################################################

try:
	import jiwer
except:

	print("\nERROR: You need to install the library \"jiwer\" in your system.")
	print("In your conda environment try with:")
	print("\n\t$ pip install jiwer\n")
	ERROR_FLAG=True
#ENDTRY

########################################################################

try:
	from faster_whisper import WhisperModel
	from recipe_scripts.transcribe_splits import transcribe_splits
	
except:

	print("\nERROR: You need to install the library \"faster-whisper\" in your system.")
	print("In your conda environment try with:")
	print("\n\t$ pip install faster-whisper\n")
	ERROR_FLAG=True
#ENDTRY

########################################################################

from recipe_scripts.download_spjallromur import download_spjallromur
from recipe_scripts.extract_spjallromur import extract_spjallromur
from recipe_scripts.rename_spjallromur import rename_spjallromur
from recipe_scripts.segment_files import segment_files
from recipe_scripts.segment_spjallromur import segment_spjallromur
from recipe_scripts.filter_spjallromur import filter_spjallromur
from recipe_scripts.spjallromur_asr import spjallromur_asr
from recipe_scripts.download_asr_model import download_asr_model
from recipe_scripts.calculate_wer import calculate_wer

########################################################################
#Check the existance of ffmpeg in the system
import subprocess

cmd="ffmpeg -version | head -n 1"
shell_out=subprocess.check_output(cmd,shell=True)

shell_out=shell_out.decode("utf-8")
shell_out=re.sub('\s+',' ',shell_out)
shell_out=shell_out.strip()
list_shell=shell_out.split(" ")

first_word=list_shell[0]
first_word_ok="ffmpeg"

if first_word!=first_word_ok:
	print("\nERROR: You need to install the command \"ffmpeg\" in your system.")
	print("In Ubuntu try with:")
	print("\n\t$ sudo apt install ffmpeg\n")
	ERROR_FLAG=True
#ENDIF

########################################################################
#Check the existance of git-lfs in the system

cmd="git-lfs -v"
shell_out=subprocess.check_output(cmd,shell=True)

shell_out=shell_out.decode("utf-8")
shell_out=shell_out[0:7]

first_word=shell_out
first_word_ok="git-lfs"

if first_word!=first_word_ok:
	print("\nERROR: You need to install the command \"git-lfs\" in your system.")
	print("In Ubuntu try with:")
	print("\n\t$ sudo apt install git-lfs\n")
	ERROR_FLAG=True
#ENDIF

########################################################################

if ERROR_FLAG==False:

	print("\n\tSuccess: Your system is ready to run the recipe!\n")
#ENDIF

########################################################################

