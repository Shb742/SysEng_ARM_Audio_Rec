#!/usr/bin/env python


"""
Dervided from
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
https://cmusphinx.github.io/wiki/tutoriallm/#using-keyword-lists-with-pocketsphinx
https://cmusphinx.github.io/wiki/tutorialdict/
"""

#arecord -v -f S16_LE -c1 -r48000 -t raw | sox -c 1 -r 48000 -b 16 -L -e signed-integer -t raw - -c 1 -r 48000 -b 16 -L -e signed-integer -t raw - vol 0 dB | rnnoise/examples/./rnn_test /dev/stdout | sox -t raw -r 48000 -b 16 -c 1 -L -e signed-integer - -t raw -r 16000 -b 16 -c 1 -L -e signed-integer - | python SpeechDetectStdIn.py
#https://raspberrypi.stackexchange.com/questions/56773/using-pocketsphinx-for-voice-control-applications

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import audioop
from collections import deque
import time
import math
import sys
import dashboard


# These will need to be modified according to where the pocketsphinx folder is
model_directory = "../Sphinx/pocketsphinx-5prealpha/model"

stream_chunk_size = 1024  # CHUNKS of bytes to read each time from mic
channels = 1
sample_rate = 16000
silence_lenght = 1.5 #The ammount of time(in seconds) before the recording is stopped and transcribed
pre_threshold_audio_legnth = 0.5  #The ammount of time(in seconds) before the threshold is crossed to send to be transcribed (avoids cutting out the beggining of the word)
threshold = 400 #Audio intensity to trigger recording of phrase
decoder = None #Placeholder

dashboard.channels = channels
dashboard.sample_rate = sample_rate

def setupDecoder():
	global decoder
	# Create a decoder with certain model
	config = Decoder.default_config()
	config.set_string('-hmm', os.path.join(model_directory, 'en-us/en-us'))
	config.set_string('-lm', os.path.join(model_directory, 'en-us/en-us.lm.bin'))
	config.set_string('-dict', 'customDict')#config.set_string('-dict', os.path.join(model_directory, 'en-us/cmudict-en-us.dict'))
	#Set up key words
	#config.set_string('-kws', 'keywords')
	#config.set_string('-keyphrase', 'help me')
	#config.set_float('-kws_threshold', 1e+20)
	#Set up keywords
	# Creaders decoder object for streaming data.
	decoder = Decoder(config)


def setAudioThreshold(num_samples=50):
	stream = sys.stdin.buffer
	values = [math.sqrt(abs(audioop.avg(stream.read(stream_chunk_size), 4))) for x in range(num_samples)]
	values = sorted(values, reverse=True)
	print(values)
	r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
	print(" Finished ")
	print(" Average audio intensity is ", r)

	if r < 3000:
		threshold = 3500 #sets upperlimit
	else:
		threshold = r + 100 #adds 100 to avoid flase triggering

def decode_phrase(data):
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

def run():
	setAudioThreshold()
	setupDecoder()
	stream = sys.stdin.buffer
	print("* Mic set up and listening. ")

	audio2send = []
	cur_data = ''  # current chunk of audio data
	rel = sample_rate/stream_chunk_size
	slid_win = deque(maxlen= int(silence_lenght * rel))
	#Prepend audio from 0.5 seconds before noise was detected
	pre_threshold_audio = deque(maxlen= int(pre_threshold_audio_legnth * rel))
	started = False

	while True:
		cur_data = stream.read(stream_chunk_size)
		slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
		if sum([x > threshold for x in slid_win]) > 0:#Edit here if we want multiple values above threshold to trigger listening
			if started == False:
				print("* Starting recording of phrase")
				started = True
			audio2send.append(cur_data)

		elif started:
			print("* Finished recording, decoding phrase")
			r = decode_phrase(list(pre_threshold_audio) + audio2send)
			if (len(r) > 0 and ( True in [ "help" in x for x in r] )):
				dashboard.send(list(pre_threshold_audio) + audio2send)
				stream.read()#get rid of old data
			print("DETECTED: ", r)
			#Reset all
			started = False
			slid_win = deque(maxlen= int(silence_lenght * rel) )
			pre_threshold_audio = deque(maxlen= int(pre_threshold_audio_legnth * rel))
			audio2send = []
			print("* Listening ...")

		else:
			pre_threshold_audio.append(cur_data)

	print("* Done listening")

if __name__ == "__main__":
	run()

