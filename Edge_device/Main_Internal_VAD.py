#!/usr/bin/env python


"""
Dervided from
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
https://cmusphinx.github.io/wiki/tutoriallm/#using-keyword-lists-with-pocketsphinx
https://cmusphinx.github.io/wiki/tutorialdict/
"""

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import audioop
from collections import deque
import time
import math
import sys
import dashboard,rnnoise
import threading

# These will need to be modified according to where the pocketsphinx folder is
model_directory = "pocketsphinx-5prealpha/model"

input_sample_rate = 48000#Do not change as rnnoise requires sample rate of 48K
input_chunk_size = 480#Do not change as rnnoise requires frame size of 480

stream_chunk_size = input_chunk_size*2#Each short is 2 bytes    #1024  # CHUNKS of bytes to read each time from mic
channels = 1
sample_rate = 16000#Do not change as sphinx requires sample rate of 16K
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
	config.set_boolean('-verbose', False)
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

import wave,io,pyaudio#Temporary for testing putposes only
def encode_speech(data):
	#globals
	global channels
	global sample_rate
	#globals*
	data = b''.join(data)[:11796400]#Save Only first ~15Mb(once base64 encoded)
	buf = open("output.wav","wb")
	wf = wave.open(buf, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()


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
		threshold = r + 100 #adds offset to avoid flase triggering

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
	#setAudioThreshold()
	setupDecoder()
	rnnoise_state = rnnoise.RNNoise()
	resampler_state = None

	stream = sys.stdin.buffer
	print("* Mic set up and listening. ")

	audio2send = []
	input_data = b''
	denoised_data = b''
	rel = sample_rate/input_chunk_size
	slid_win = deque(maxlen= int(silence_lenght * rel))
	voice_activity = deque(maxlen=int(silence_lenght * rel))
	#Prepend audio from 0.5 seconds before noise was detected
	pre_threshold_audio = deque(maxlen= int(pre_threshold_audio_legnth * rel))
	started = False

	pinger = threading.Thread(target=dashboard.ping)
	pinger.daemon = True  # thread dies with main thread (the only non-daemon thread)
	pinger.start()

	try:
		while True:
			input_data = stream.read(stream_chunk_size)
			VodProb,denoised_data = rnnoise_state.process_frame(input_data)
			voice_activity.append(VodProb)
			#input_data,resampler_state = audioop.ratecv(input_data,4,1,input_sample_rate,16000,resampler_state)#If we want to resample audio input
			denoised_data,resampler_state = audioop.ratecv(denoised_data,4,1,input_sample_rate,sample_rate,resampler_state)
			slid_win.append(math.sqrt(abs(audioop.avg(denoised_data, 4))))
			#print(max(voice_activity))
			#print("-------")	

			if max(voice_activity) > 0.5:
				if started == False:
					print("* Starting recording of phrase")
					started = True
				audio2send.append(denoised_data)
			elif started:
				print("* Finished recording, decoding phrase")
				r = decode_phrase(list(pre_threshold_audio) + audio2send)
				encode_speech((list(pre_threshold_audio) + audio2send))
				if (len(r) > 0 and ( True in [ "help" in x for x in r] )):
				 	dashboard.send((list(pre_threshold_audio) + audio2send),r )
				print("DETECTED: ", r)
				#Reset all
				started = False
				slid_win = deque(maxlen= int(silence_lenght * rel) )
				pre_threshold_audio = deque(maxlen= int(pre_threshold_audio_legnth * rel))
				audio2send = []
				print("* Listening ...")

			else:
				pre_threshold_audio.append(denoised_data)
	except Exception as e:
		print(e)
	rnnoise_state.destroy()
	print("* Done listening")

if __name__ == "__main__":
	run()

