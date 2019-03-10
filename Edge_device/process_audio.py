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


#keywords = ["help"]#maybe load keyphrase_list
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
	global keywords

	init_decoder()
	init_dashboard()

	while 1:
		audio = jobs.get()#blocking call, waiting for jobs
		decoded_text = decode_audio(audio)
		print("DETECTED: ", decoded_text)
		if (len(decoded_text) > 0):
			dashboard.send(audio,decoded_text)