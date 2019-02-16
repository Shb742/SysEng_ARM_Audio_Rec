#!/usr/bin/env python3
import wave,io,time#Temporary for testing putposes only
def encode_speech(data,sample_rate,name="fp"):
	#globals
	global channels
	#globals*
	data = data[:11796400]#Save Only first ~15Mb(once base64 encoded)
	#buf = open("test/samples/"+name+" - "+str(time.time())+".wav","wb")
	wf = wave.open("test/samples/"+name+" - "+str(time.time())+".wav", 'wb')
	wf.setnchannels(1)
	wf.setsampwidth(2)#16bit
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()

import audioop
class WaveReader(object):
	def __init__(self, obj):
		self.obj = obj
		self.channels=self.obj.getnchannels()
		self.sw = self.obj.getsampwidth()
		self.sf = self.obj.getframerate()
		self.resampler_state = None

	def read(self,frames):
		data = self.obj.readframes((frames//self.channels))
		#data = data[:frames]#Hack don't know why but is returning extra frames
		if (len(data) == 0 ):
			raise EOFError("reached the end")
		if (self.sw != 2):
			data = audioop.lin2lin(data, self.sw, 2)
		if (self.channels == 2):
			data = audioop.tomono(data, 2, 1, 1)
		if (self.sf != 48000):
			data,self.resampler_state = audioop.ratecv(data,2,1,self.sf,48000,self.resampler_state)
		data = data[:frames]#Hack don't know why but is returning extra frames
		return data #returns data formatted as 48Khz 16bit mono
	def close(self):
		self.obj.close()

import math
def getVolume(samples):
	num_samples = int(len(samples)/1024)
	values = [math.sqrt(abs(audioop.avg(samples[1024*x:1024*(x+1)], 2))) for x in range(num_samples)]
	values = sorted(values, reverse=True)
	#print(values)
	return sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
	
def adjustVolume(fragment,new_vol):
	vol = getVolume(fragment)
	#print("old vol : " + str(vol))
	inc = ((new_vol/vol) < 1.0)
	if (inc):
		while (vol > (new_vol+1) ):
			fragment = audioop.mul(fragment, 2, new_vol/vol) #Volume down/up if needed
			vol = getVolume(fragment)
	else:
		while (vol < (new_vol-1) ):
			fragment = audioop.mul(fragment, 2, new_vol/vol) #Volume down/up if needed
			vol = getVolume(fragment)
	#print(" new vol :"+str(vol))
	return fragment
import os

def getWavs(dirName):
	listOfFiles = os.listdir(dirName)
	wavs = []
	for file in listOfFiles:
		fullPath = os.path.join(dirName, file)
		if os.path.isdir(fullPath):
			wavs = wavs + getWavs(fullPath)
		elif (".wav" in fullPath):
			wavs.append(fullPath)  
	return wavs

import random
import wave
import rnnoise, process_audio

def test_normalize_volume(x):
	rnnoise_state = rnnoise.RNNoise()
	resampler_state = None

	r1 = random.Random()
	r2 = random.Random()
	r1.seed(83782625373708)#So we get same seq every time
	r2.seed(52552468426257)#So we get same seq every time


	input_sample_rate = 48000#Do not change as rnnoise requires sample rate of 48K
	sample_rate = 16000#Do not change as sphinx requires sample rate of 16K
	input_chunk_size = 480#Do not change as rnnoise requires frame size of 480
	input_sample_width = 2#16 bit, each short is 2 bytes
	audio_sample_density = (input_sample_rate/input_chunk_size) #i.e chunks for a second
	THREE_SECONDS_CHUNKED = int(audio_sample_density*3)
	THREE_SECONDS = int(input_chunk_size*input_sample_width*THREE_SECONDS_CHUNKED)

	noise_path = "test/noise"
	noise_wavs = getWavs(noise_path)
	MAX_NOISE_VOL = 7
	BACKGROUND_SPEECH_VOL = 2
	SPEECH_VOL_MIN = 9
	SPEECH_VOL_MAX = 12
	DENOISED_VOL = 3
	fp_path = "test/false_samples"
	fp_wavs = getWavs(fp_path)

	tp_path = "test/true_samples/"
	tp_wavs = getWavs(tp_path)


	true_positive_count = 0#Sample had key-phrase and was detected
	false_negative_count = 0#Sample had key-phrase but wasn't detected

	false_positive_count = 0#Sample had no key-phrase, but was detected
	true_negative_count = 0#Sample had no key-phrase and wasn't detected


	import sys

	if ("-lf" in sys.argv):
		print(noise_wavs)
		print(fp_wavs)
		print(tp_wavs)
		input("press enter to continue..")

	verbose = ("-v" in sys.argv)
	save_true_positives = ("-savetp" in sys.argv)
	save_false_positives = ("-savefp" in sys.argv)
	save_true_negatives = ("-savetn" in sys.argv)
	save_false_negatives = ("-savefn" in sys.argv)

	process_audio.init_decoder()
	progress = 0
	smaller_prog = 0
	try:
		for noise_wav in noise_wavs:
			noise_stream = WaveReader(wave.open(noise_wav, 'rb'))
			noise_data = noise_stream.read(THREE_SECONDS)
			noise_stream.close()
			if (verbose):
				print(noise_wav.split("/")[-1])
			else:
				print(smaller_prog*100.0)
			if (getVolume(noise_data) > MAX_NOISE_VOL):
				noise_data = adjustVolume(noise_data,MAX_NOISE_VOL)
			for fp_wav in fp_wavs:
				#continue#tmp
				fp_stream = WaveReader(wave.open(fp_wav, 'rb'))
				data = fp_stream.read(len(noise_data))
				fp_stream.close()
				name = "fp"
				speech = None
				if ((r1.random()<=0.25) and (len(data) == THREE_SECONDS) ):#add true positives, 35% prob
					data = adjustVolume(data,BACKGROUND_SPEECH_VOL)#move false speech to background
					tp_stream = WaveReader(wave.open((r2.choice(tp_wavs)), 'rb'))
					speech = tp_stream.read(len(data))
					tp_stream.close()
					speech = adjustVolume(speech,r1.uniform(SPEECH_VOL_MIN,SPEECH_VOL_MAX))#set speech at apt vol
					data = audioop.add(data,speech,input_sample_width)
					name = "fp_tp"
				else:
					data = adjustVolume(data,r1.uniform(SPEECH_VOL_MIN,SPEECH_VOL_MAX))#set speech at apt vol
				data = audioop.add(noise_data,data,input_sample_width)#add noise
				denoised_data = b''
				for i in range(THREE_SECONDS_CHUNKED):
					VodProb,a = rnnoise_state.process_frame(data[(input_chunk_size*input_sample_width*i):(input_chunk_size*input_sample_width*(i+1))])
					denoised_data += a
				denoised_data = adjustVolume(denoised_data,DENOISED_VOL)
				denoised_data,resampler_state = audioop.ratecv(denoised_data,input_sample_width,1,input_sample_rate,sample_rate,resampler_state)
				result = process_audio.decode_audio(denoised_data)
				if (len(result)>0):#detected
					if (name == "fp_tp"):
						true_positive_count+=1#add true_positive
						if (save_true_positives):
							encode_speech(data,input_sample_rate,"true positive")
					else:
						false_positive_count+=1#add false_positive
						if (save_false_positives):
							encode_speech(data,input_sample_rate,"false positive"+str(result).replace("[","").replace("]"," "))
				else:
					if (name == "fp_tp"):
						false_negative_count+=1#add false_negative
						if (save_false_negatives):
							#encode_speech(data,input_sample_rate,"false negative")
							#encode_speech(speech,input_sample_rate,"false negative_inp")
							encode_speech(denoised_data,sample_rate,"false negative")
					else:
						true_negative_count+=1#add true_negative_count
						if (save_true_negatives):
							encode_speech(data,input_sample_rate,"true negative")
				smaller_prog += 1.0/((len(fp_wavs)+len(tp_wavs))*(len(noise_wavs)))
				if (verbose):
					print(result)
					print(smaller_prog*100.0)

			for tp_wav in tp_wavs:
				#continue#tmp
				tp_stream = WaveReader(wave.open(tp_wav, 'rb'))
				if (verbose):
					print(tp_wav)
				data = tp_stream.read(len(noise_data))
				data = adjustVolume(data,r1.uniform(SPEECH_VOL_MIN,SPEECH_VOL_MAX))
				data = audioop.add(noise_data,data,input_sample_width)
				tp_stream.close()
				denoised_data = b''
				for i in range(THREE_SECONDS_CHUNKED):
					VodProb,a = rnnoise_state.process_frame(data[(input_chunk_size*input_sample_width*i):(input_chunk_size*input_sample_width*(i+1))])
					denoised_data += a
				denoised_data = adjustVolume(denoised_data,DENOISED_VOL)
				denoised_data,resampler_state = audioop.ratecv(denoised_data,input_sample_width,1,input_sample_rate,sample_rate,resampler_state)
				#denoised_data = adjustVolume(denoised_data,DENOISED_VOL)
				result = process_audio.decode_audio(denoised_data)
				if (len(result)>0):#detected
					true_positive_count+=1#add true_positive
					if (save_true_positives):
						encode_speech(data,input_sample_rate,"tp")
						#encode_speech(denoised_data,sample_rate,"tp_dn")
				else:
					false_negative_count+=1#add false_negative
					if (save_false_negatives):
						encode_speech(data,input_sample_rate,"fn")
						#encode_speech(denoised_data,sample_rate,"fn_dn")
				smaller_prog += 1.0/((len(fp_wavs)+len(tp_wavs))*(len(noise_wavs)))
				if (verbose):
					print(result)
					print(smaller_prog*100.0)
				
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		print("probably ctrl-c")

	total_count = false_positive_count+true_negative_count+false_negative_count+true_positive_count
	print("true positives : - "+str(true_positive_count))
	print("false negatives : - "+str(false_negative_count))

	print("false positives : - "+str(false_positive_count))
	print("true negatives : - "+str(true_negative_count))
	print("total :- "+str(total_count))

	fpr = 0.0
	tpr = 0.0
	ppv = 0.0
	try:
		fpr = (false_positive_count/(true_negative_count+false_positive_count))# false_positive_rate
	except Exception as e:
		print(e)
	try:
		tpr = (true_positive_count/(true_positive_count+false_negative_count))# true_positive_rate 
	except Exception as e:
		print(e)
	try:
		ppv = (true_positive_count/(true_positive_count+false_positive_count))# positive predictive value
	except Exception as e:
		print(e)

	print("false positive rate : - "+str(fpr))
	print("true positive rate : - "+str(tpr)) 
	print("positive predictive value : - "+str(ppv))
	return (fpr,tpr,ppv)



test_normalize_volume(0)
def get_data(x_min,x_max,x_step):
	tpr_points = []
	fpr_points = []
	ppv_points = []
	for i in range(((x_max-x_min)//x_step)):
		f,t,p = test_normalize_volume(x_min+(x_step*i))
		tpr_points.append(t)
		fpr_points.append(f)
		ppv_points.append(p)
		print("Total_Progress ="+str((i/((x_max-x_min)//x_step))))
	return (tpr_points,fpr_points,ppv_points)
import matplotlib.pyplot as plt
import numpy as np


#Get values
#tpr_points, fpr_points,ppv_points = get_data(0,25,1)

# tpr_points.append(1.0)
# fpr_points.append(1.0)
# ppv_points.append(0.0)

print(tpr_points)
print(fpr_points)
print (ppv_points)
# This is the AUC
auc = abs(np.trapz(tpr_points,fpr_points))
print("Area Under Curve - "+str(auc))


title = "test_normalize_volume"
plt.figure(title)
# This is the ROC curve
plt.subplot(211)
plt.title("ROC curve")
plt.xlim([0, 1])
plt.ylim([0, 1])
#Plot no skill
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr_points,tpr_points,'r-.')
plt.ylabel("True positive rate")
plt.xlabel("False positive rate")
#plt.gca().invert_xaxis()#inver x axis so it makes sense

plt.subplot(212)
plt.title("PRC curve")
plt.xlim([0, 1])
plt.ylim([0, 1])
# plot no skill
plt.plot([0, 1], [0.5, 0.5], linestyle='--')
plt.plot(tpr_points,ppv_points,'r-.')
plt.ylabel("Positive predictive value")
plt.xlabel("True positive rate")


plt.show() 


