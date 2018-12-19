#python mystt.py models/output_graph.pb models/alphabet.txt /tmp/input1.wav
from deepspeech.model import Model
import scipy.io.wavfile as wav
import sys
ds = Model("models/output_graph.pb", 26, 9, "models/alphabet.txt", 500)
fs, audio = wav.read(sys.argv[3])
processed_data = ds.stt(audio, fs)
print(processed_data)

#with open('/tmp/data.txt', 'a') as f:
#    f.write(processed_data)

