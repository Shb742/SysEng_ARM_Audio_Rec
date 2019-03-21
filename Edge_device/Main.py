#!/usr/bin/env python3


"""
Dervided from
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
"""

import audioop
from collections import deque
import time
import math
import sys
import rnnoise, process_audio
import multiprocessing


input_sample_rate = 48000#Do not change as rnnoise requires sample rate of 48K
input_chunk_size = 480#Do not change as rnnoise requires frame size of 480
input_sample_width = 2#16 bit, each short is 2 bytes

stream_chunk_size = input_chunk_size*input_sample_width
channels = 1
sample_rate = 16000#Do not change as sphinx requires sample rate of 16K
silence_lenght = 1.5 #The ammount of time(in seconds) before the recording is stopped and transcribed
segment_lenght = 3 #The ammount of time(in seconds) which the audio stream is split into when being processed
pre_threshold_audio_legnth = 0.5  #The ammount of time(in seconds) before the threshold is crossed to send to be transcribed (avoids cutting out the beggining of the word)
threshold = 20 #Audio intensity to trigger knock detection
denoised_volume = 3#set the intensity of the audio sample


#Setup variables
resampler_state = None
decoder_queue = multiprocessing.SimpleQueue()
audio_sample_density = (input_sample_rate/input_chunk_size)
#Prepend audio from seconds before activity was detected
pre_threshold_audio_legnth = int(pre_threshold_audio_legnth*audio_sample_density)
pre_threshold_raw_audio_legnth = int(0.2*audio_sample_density)
#Chunk audio to be processed into segments
segment_lenght = int(segment_lenght*audio_sample_density)

import wave,io#Temporary for testing putposes only
def encode_speech(data):
	#globals
	global channels
	global sample_rate
	global input_sample_width
	#globals*
	data = data[:11796400]#Save Only first ~15Mb(once base64 encoded)
	buf = open("output"+str(time.time())+".wav","wb")
	wf = wave.open(buf, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(input_sample_width)#16bit
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()

def getVolume(samples):
	num_samples = int(len(samples)/1024)
	values = [math.sqrt(abs(audioop.avg(samples[1024*x:1024*(x+1)], 2))) for x in range(num_samples)]
	values = sorted(values, reverse=True)
	return sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
	
def adjustVolume(fragment):
	global denoised_volume
	global input_sample_width
	vol = getVolume(fragment)
	inc = ((denoised_volume/vol) < 1.0)
	if (inc):
		while (vol > (denoised_volume+1) ):
			fragment = audioop.mul(fragment, input_sample_width, denoised_volume/vol) #Volume down/up if needed
			vol = getVolume(fragment)
	else:
		while (vol < (denoised_volume-1) ):
			fragment = audioop.mul(fragment, input_sample_width, denoised_volume/vol) #Volume down/up if needed
			vol = getVolume(fragment)
	return fragment

#def setAudioThreshold(num_samples=50):
	# values = [math.sqrt(abs(audioop.avg(stream.read(stream_chunk_size), 2))) for x in range(num_samples)]
	# values = sorted(values, reverse=True)
	# print(values)
	# r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
	# print(" Finished ")
	# print(" Average audio intensity is ", r)

	# if r < 3000:
	# 	threshold = 3500 #sets upperlimit
	# else:
	# 	threshold = r + 100 #adds offset to avoid flase triggering

def queAudio(pre_threshold_audio,audio_to_send,segment_lenght,voice=1):
	global pre_threshold_audio_legnth, pre_threshold_raw_audio_legnth
	global input_sample_width
	global channels
	global input_sample_rate, sample_rate
	global resampler_state
	global decoder_queue
	if ((len(audio_to_send)+len(pre_threshold_audio))>segment_lenght):
		tmp = adjustVolume(b''.join(list(pre_threshold_audio)+audio_to_send))#should be in full 3 second clip
		tmp,resampler_state = audioop.ratecv(tmp,input_sample_width,channels,input_sample_rate,sample_rate,resampler_state)
		decoder_queue.put((voice,tmp))
		pre_threshold_audio.clear()
		#Keep bit of previous segment
		if (voice):
			audio_to_send = audio_to_send[int(len(audio_to_send)-pre_threshold_audio_legnth):]
		else:
			audio_to_send = audio_to_send[int(len(audio_to_send)-pre_threshold_raw_audio_legnth):]
	return (pre_threshold_audio,audio_to_send)

def main():
	#Globals
	global threshold
	global input_sample_width
	global silence_lenght
	global decoder_queue
	global segment_lenght

	#Setup decoder proc
	decoder_proc = multiprocessing.Process(target=process_audio.main, args=(decoder_queue,))
	decoder_proc.start()

	#Noise removal
	rnnoise_state = rnnoise.RNNoise()

	#Event detection setup
	voice_activity = deque(maxlen=int(silence_lenght * audio_sample_density))
	slid_win = deque(maxlen= int(silence_lenght * audio_sample_density))


	#Place holders
	pre_threshold_audio = deque(maxlen=pre_threshold_audio_legnth)
	pre_threshold_raw_audio = deque(maxlen=pre_threshold_raw_audio_legnth)
	audio_to_send = []
	raw_audio_to_send = []
	input_data = b''
	denoised_data = b''
	
	#Setup loop vars
	started = False
	started_raw = False
	stream = sys.stdin.buffer
	print("* Mic set up and listening. ")
	try:
		while True:
			input_data = stream.read(stream_chunk_size)
			VodProb,denoised_data = rnnoise_state.process_frame(input_data)
			voice_activity.append(VodProb)
			#input_data,resampler_state = audioop.ratecv(input_data,input_sample_width,1,input_sample_rate,16000,resampler_state)#If we want to resample audio input
			slid_win.append(math.sqrt(abs(audioop.avg(input_data, input_sample_width))))
			#print(max(voice_activity))
			#print("-------")	
			VodProb = max(voice_activity)
			#print(max(slid_win))
			#threshold_cross = sum([x > threshold for x in slid_win]) > 0
			if (VodProb > 0.5) :
				if started == False:
					print("* Starting recording of phrase")
					started = True
				audio_to_send.append(denoised_data)
				pre_threshold_audio,audio_to_send = queAudio(pre_threshold_audio,audio_to_send,segment_lenght)
			elif started:
				pre_threshold_audio,audio_to_send = queAudio(pre_threshold_audio,audio_to_send,0)
				print("* Finished recording, decoding phrase")
				#Reset all
				started = False
				print("* Listening for speech...")
			else:
				pre_threshold_audio.append(denoised_data)
			if (sum([x > threshold for x in slid_win]) > 0):
				if started_raw == False:
					print("* Starting recording of sound")
					started_raw = True
				raw_audio_to_send.append(input_data)
				raw_pre_threshold_audio,raw_audio_to_send = queAudio(pre_threshold_raw_audio,raw_audio_to_send,segment_lenght,voice=0)
			elif (started_raw):
				queAudio(pre_threshold_raw_audio,raw_audio_to_send,0,voice=0)
				print("* Finished recording, decoding sound")
				#Reset all
				started_raw = False
				slid_win.clear()
				pre_threshold_raw_audio.clear()
				raw_audio_to_send = []
				print("* Listening ...")
			else:
				pre_threshold_raw_audio.append(input_data)
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		print("probably ctrl-c")
	#exit routine
	decoder_proc.terminate()
	decoder_proc.join()
	rnnoise_state.destroy()
	print("* Done listening")

if __name__ == "__main__":
	main()

