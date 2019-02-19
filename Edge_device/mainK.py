#!/usr/bin/env python3


"""
Dervided from
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
https://cmusphinx.github.io/wiki/tutoriallm/#using-keyword-lists-with-pocketsphinx
https://cmusphinx.github.io/wiki/tutorialdict/
"""

import audioop
from collections import deque
import time
import math
import sys
import rnnoise, process_audio
import multiprocessing
from analyze.py import *
from worker.py import *


input_sample_rate = 48000#Do not change as rnnoise requires sample rate of 48K
input_chunk_size = 480#Do not change as rnnoise requires frame size of 480

stream_chunk_size = input_chunk_size*2#Each short is 2 bytes    #1024  # CHUNKS of bytes to read each time from mic
channels = 1
sample_rate = 16000#Do not change as sphinx requires sample rate of 16K
silence_lenght = 1.5 #The ammount of time(in seconds) before the recording is stopped and transcribed
segment_lenght = 3 #The ammount of time(in seconds) which the audio stream is split into when being processed
pre_threshold_audio_legnth = 0.5  #The ammount of time(in seconds) before the threshold is crossed to send to be transcribed (avoids cutting out the beggining of the word)
threshold = 400 #Audio intensity to trigger recording of phrase


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


def main():
	global pre_threshold_audio_legnth
	global segment_lenght
	decoder_queue = multiprocessing.SimpleQueue()
	decoder_proc = multiprocessing.Process(target=process_audio.main, args=(decoder_queue,))
	decoder_proc.start()

	#Noise removal and resampler
	rnnoise_state = rnnoise.RNNoise()
	resampler_state = None

	audio2send = []
	input_data = b''
	denoised_data = b''

	#Event detection setup
	audio_sample_density = (input_sample_rate/input_chunk_size)
	slid_win = deque(maxlen= int(silence_lenght * audio_sample_density))
	voice_activity = deque(maxlen=int(silence_lenght * audio_sample_density))
	#Prepend audio from 0.5 seconds before noise was detected
	pre_threshold_audio_legnth = int(pre_threshold_audio_legnth*audio_sample_density)
	pre_threshold_audio = deque(maxlen=pre_threshold_audio_legnth)
	#Chunk audio to be processed into segments
	segment_lenght = int(segment_lenght*audio_sample_density)

	started = False
	stream = sys.stdin.buffer
	print("* Mic set up and listening. ")
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

				if (len(audio2send)>segment_lenght):
					decoder_queue.put(list(pre_threshold_audio) + audio2send)
					#encode_speech(list(pre_threshold_audio) + audio2send)
					#time.sleep(1000)
					pre_threshold_audio.clear()
					audio2send = audio2send[int(len(audio2send)-pre_threshold_audio_legnth):]#Keep bit of previous segment
			elif started:
				print("* Finished recording, decoding phrase")
				decoder_queue.put(list(pre_threshold_audio) + audio2send)
				#Reset all
				started = False
				slid_win.clear()
				pre_threshold_audio.clear()
				audio2send = []
				print("* Listening ...")

			else:
				pre_threshold_audio.append(denoised_data)
	except Exception as e:
		print(e)
	decoder_proc.terminate()
	decoder_proc.join()
	rnnoise_state.destroy()
	print("* Done listening")

if __name__ == "__main__":
	main()
