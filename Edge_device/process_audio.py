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


keywords = ["help"]
model_directory = "pocketsphinx-5prealpha/model"
decoder = None #Placeholder
pinger = None #Placeholder

def init_dashboard():
	global pinger
	dashboard.channels = 1
	dashboard.sample_rate = 16000
	pinger = threading.Thread(target=dashboard.ping)
	pinger.daemon = True  # thread dies with main thread (the only non-daemon thread)
	pinger.start()

def init_decoder():
	global decoder
	config = Decoder.default_config()
	config.set_boolean('-verbose', False)
	config.set_string('-logfn', "/dev/null")
	config.set_string('-hmm', os.path.join(model_directory, 'en-us/en-us'))
	config.set_string('-lm', os.path.join(model_directory, 'en-us/en-us.lm.bin'))
	config.set_string('-dict', os.path.join(model_directory, 'en-us/cmudict-en-us.dict'))
	#config.set_string('-dict', 'customDict')#config.set_string('-dict', os.path.join(model_directory, 'en-us/cmudict-en-us.dict'))
	#Set up key words
	#config.set_string('-kws', 'keywords')
	#config.set_string('-keyphrase', 'help me')
	#config.set_float('-kws_threshold', 1e+20)
	#Set up keywords
	# Creaders decoder object for streaming data.
	decoder = Decoder(config)

def decode_audio(data):
	global decoder
	decoder.start_utt()
	data = b''.join(data)
	while True:
		buf = data[:1024]
		data = data[1024:]
		if buf:
			decoder.process_raw(buf, False, False)
			#if self.decoder.hyp() != None:
			#    print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
			#    print ("Detected keyword")
		else:
			break
	decoder.end_utt()
	words = []
	[words.append(seg.word) for seg in decoder.seg()]
	return words

def main(jobs):
	global keywords

	init_decoder()
	init_dashboard()
	while 1:
		audio = jobs.get()
		decoded_text = decode_audio(audio)
		print("DETECTED: ", decoded_text)
		if (len(decoded_text) > 0 and ( True in [ (x in keywords) for x in decoded_text] )):
			dashboard.send(audio,decoded_text)