import audioTrainTest as aT
import numpy as np
classifier_info  = ("gradientboosting_classifier","gradientboosting")
path = "/home/shoaib/sf_CodeUCL/Year_2/Systems_Eng/Main/Project/Experimental_Features/Shoaib/knock_detector/knocking/train/"
files = getWavs("/home/shoaib/sf_CodeUCL/Year_2/Systems_Eng/Main/Project/Experimental_Features/Shoaib/knock_detector/knocking/test/")
aT.featureAndTrain([path+"false",path+"true"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, classifier_info[1], classifier_info[0], False)


input_sample_rate = 48000#Do not change as rnnoise requires sample rate of 48K
sample_rate = 16000#Do not change as sphinx requires sample rate of 16K
input_chunk_size = 480#Do not change as rnnoise requires frame size of 480
input_sample_width = 2#16 bit, each short is 2 bytes
audio_sample_density = (input_sample_rate/input_chunk_size) #i.e chunks for a second
THREE_SECONDS_CHUNKED = int(audio_sample_density*3)
THREE_SECONDS = int(input_chunk_size*input_sample_width*THREE_SECONDS_CHUNKED)

import wave
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
		if (self.sf != 16000):
			data,self.resampler_state = audioop.ratecv(data,2,1,self.sf,16000,self.resampler_state)
		data = data[:frames]#Hack don't know why but is returning extra frames
		return data #returns data formatted as 48Khz 16bit mono
	def close(self):
		self.obj.close()

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

classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat = [None]*9

def init_classifier():
	global classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat
	[classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat] = aT.load_model(classifier_info[0])
init_classifier()

import time
time_st = time.time()
acc = 0.0
count = 0.0
for file in files:
	print(count*100.0/len(files))
	stream = WaveReader(wave.open(file, 'rb'))
	data = stream.read(THREE_SECONDS)
	stream.close()
	res = aT.loaded_soundClassification(data, sample_rate, classifier_info[1],classifier, MEAN, STD, classNames, mt_win, mt_step, st_win, st_step, compute_beat)
	#res = aT.soundClassification(data, sample_rate, "svm_classifier","svm")
	#if (res[0] != np.argmax(res[1])):
	#	print(res[2][int(np.argmax(res[1]))])
	if ((("true" in res[2][int(res[0])]) and ("true" in file.split("/")[-2])) or (("false" in res[2][int(res[0])]) and ("false" in file.split("/")[-2]))):
		acc+=1.0
	count+=1.0
	##print(res)
	#print("----")
	#if (res[2][int(res[0])] == fal)
	#if (input("quit? ") == "y"):
	#	break
print(str((time.time()-time_st)/len(files))+"s per file")
print ( acc/len(files) * 100.0)
print("number of files: "+str(len(files)))
print(acc)