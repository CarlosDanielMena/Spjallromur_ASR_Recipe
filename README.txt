---------------------------------------------------------------------
                    Spjallromur ASR Recipe
---------------------------------------------------------------------

Author: Carlos Daniel Hernández Mena, Jón Guðnason
Contact: jg@ru.is
Location: Reykjavík University, Language and Voice Lab. (LVL)

---------------------------------------------------------------------
Description
---------------------------------------------------------------------

The "Spjallromur ASR Recipe" is a Python recipe destined to download 
the speech corpus "Spjallromur - Icelandic Conversational Speech 
22.01" and convert it to an ASR corpus with train, dev and test 
splits. After the conversion, the recipe performs speech recognition 
on the test and dev splits of the converted corpus using 
Faster-Whisper. Word Error Rate (WER) results are shown in terminal 
at the end of the recipe execution.

- "Spjallromur - Icelandic Conversational Speech 22.01"
http://hdl.handle.net/20.500.12537/187

- Faster-Whisper GitHub Repo
https://github.com/guillaumekln/faster-whisper

- Model used to transcribe the data
https://huggingface.co/language-and-voice-lab/whisper-large-icelandic-30k-steps-1000h-ct2

---------------------------------------------------------------------
Disclaimer and Terms of Use
---------------------------------------------------------------------

"Spjallromur ASR Recipe" by Carlos Daniel Hernández Mena and Jón 
Guðnason is licensed under a GNU General Public License v3.0 with 
the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  

To view a copy of this license visit:
https://www.gnu.org/licenses/gpl-3.0.html

---------------------------------------------------------------------
Installation and Requirements
---------------------------------------------------------------------
- You have to install the following software in your system:

* ffmpeg
* git-lfs

In Ubuntu, you can do:

	$ sudo apt install ffmpeg
	$ sudo apt install git-lfs

- It is recommended to create a conda environment for the recipe

	$ conda create -n spjallromur_asr python=3.9 anaconda

- Activate the environment

	$ conda activate spjallromur_asr

- Install Requirements

	$ pip install jiwer

	$ pip install faster-whisper

---------------------------------------------------------------------
Test Installation
---------------------------------------------------------------------

- Activate your conda environment

	$ conda activate spjallromur_asr

- Go to the main folder "Spjallromur_ASR_Recipe"

	$ cd Spjallromur_ASR_Recipe
	
- Run the script check_dependencies.py

	$ python check_dependencies.py
	
- If you see the message:

	Success: Your system is ready to run the recipe!
	
Then you can run the recipe safely. if not, you will have to
solve the issues based on the error messages that you will see 
in the terminal.

---------------------------------------------------------------------
Choose between GPU or CPU execution.
---------------------------------------------------------------------

Faster-Whisper allows users the use of either GPU or CPU execution
when transcribing audio recordings (inference). By default, this 
recipe performs CPU execution. However, to switch to GPU execution
go to the file "./recipe_scripts/transcribe_splits.py" inside the
main folder "Spjallromur_ASR_Recipe". You will see the following
Python definition:

def whisper_fast_model_conf():

	# Run on GPU with FP16
	#model = WhisperModel(FASTER_WHISPER_MODEL, device="cuda", compute_type="float16")
	# or run on GPU with INT8
	#model = WhisperModel(FASTER_WHISPER_MODEL, device="cuda", compute_type="int8_float16")
	# or run on CPU with INT8
	model = WhisperModel(FASTER_WHISPER_MODEL, device="cpu", compute_type="int8")

	return model
#ENDDEF

To change to another type of execution, just uncomment the desired
option while keeping commented the rest of them.

---------------------------------------------------------------------
Run the Recipe
---------------------------------------------------------------------

- Activate your conda environment

	$ conda activate spjallromur_asr

- Go to the main folder "Spjallromur_ASR_Recipe"

	$ cd Spjallromur_ASR_Recipe
	
- Run the script run_recipe.py

	$ python run_recipe.py

---------------------------------------------------------------------
Inspecting the Outcomes of the Recipe
---------------------------------------------------------------------
	
At the end of the recipe execution, you will see the WER results in 
the terminal. You will also see the following files:

- ./RESULTS.txt

It contains the WER results that are shown in terminal.

- ./resulting_transcriptions

This folder contains the files "RESULTING_TEST.trans" and 
"RESULTING_DEV.trans" with the transcriptions produced by 
faster-whisper.

- ./corpus_versions/spjallromur_asr

The folder "spjallromur_asr" contains the ASR corpus which is the 
result of the transformation (by this recipe) of the corpus 
"Spjallromur - Icelandic Conversational Speech 22.01" into a corpus 
suited to perform ASR experiments.

The splits of "spjallromur_asr" are as follows:

	- Train : 5815 recordings | 08h27m
	- Test  :  800 recordings | 01h02m
	- Dev   :  800 recordings | 01h04m
	- Total : 7415 recordings | 10h34m
	
- ./corpus_versions/spjallromur_asr/files

This folder contains the reference transcriptions of each split
of the corpus, as well as the files specifying absolute paths to 
each recording.
	
---------------------------------------------------------------------
Acknowledgements
---------------------------------------------------------------------

This project was funded by the Language Technology Programme for 
Icelandic 2019-2023. The programme, which is managed and coordinated 
by Almannarómur, is funded by the Icelandic Ministry of Education, 
Science and Culture.

---------------------------------------------------------------------
---------------------------------------------------------------------
        For more information about us, visit our websites
                      https://lvl.ru.is/
         https://huggingface.co/language-and-voice-lab
---------------------------------------------------------------------
---------------------------------------------------------------------

