#!/usr/bin/env python3
"""
Dervided from
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
https://cmusphinx.github.io/wiki/tutoriallm/#using-keyword-lists-with-pocketsphinx
https://cmusphinx.github.io/wiki/tutorialdict/
"""


from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import os
import threading
import dashboard

import knock_classifier.audioTrainTest as aT
import numpy as np

classifier_info  = ("knock_classifier/gradientboosting_classifier","gradientboosting")#("knock_classifier/svm_classifier","svm")
classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat = [None]*9
model_directory = "pocketsphinx-5prealpha/model"
decoder = None #Placeholder
pinger = None #Placeholder

def init_dashboard():
	global pinger
	dashboard.channels = 1
	dashboard.sample_rate = 16000
	dashboard.sample_width = 2
	pinger = threading.Thread(target=dashboard.ping)
	pinger.daemon = True  # thread dies with main thread (the only non-daemon thread)
	pinger.start()

def init_decoder():
	global decoder
	config = Decoder.default_config()
	config.set_boolean('-verbose', False)
	config.set_string('-logfn', "/dev/null")
	config.set_string('-hmm', os.path.join(model_directory, 'en-us/en-us'))
	#If processing free form language #config.set_string('-lm', os.path.join(model_directory, 'en-us/en-us.lm.bin'))
	#Original dictionary #config.set_string('-dict', os.path.join(model_directory, 'en-us/cmudict-en-us.dict'))
	config.set_string('-dict', 'customDict')

	#Load keyphrase_list
	dashboard.load_kws()

	# Creaders decoder object for streaming data.
	decoder = Decoder(config)
	decoder.set_kws('keyphrase', 'keyphrase_list')
	decoder.set_search('keyphrase')

def init_classifier():
	global classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat
	[classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat] = aT.load_model(classifier_info[0])


def decode_audio(data):
	global decoder
	#data = b''.join(data)
	buf = data[:1024]
	data = data[1024:]
	decoder.start_utt()
	while buf:
		decoder.process_raw(buf, False, False)
		buf = data[:1024]
		data = data[1024:]
	decoder.end_utt()
	words = []
	[words.append(seg.word) for seg in decoder.seg()]
	return words

def main(jobs):
	global classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat
	global classifier_info

	init_decoder()
	init_dashboard()
	init_classifier()

	while 1:
		audio = jobs.get()#blocking call, waiting for jobs
		if (audio[0]):
			decoded_text = decode_audio(audio[1])
			if (decoded_text != []):
				print("DETECTED: ", decoded_text)
			if (len(decoded_text) > 0):
				dashboard.send(audio[1],decoded_text)
		else:
			res = aT.loaded_soundClassification(audio[1], 16000, classifier_info[1], classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat)
			if (res[0] != -1):
				res = res[2][int(res[0])]
				if (res   == "true"):
					print("DETECTED: knock")