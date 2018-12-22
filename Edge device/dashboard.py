import requests,json,base64
import wave


#Load env vars
env_vars = {}
with open(".env") as f:
    for line in f:
        if line.startswith('#'):
            continue
        # if 'export' not in line:
        #     continue
        # Remove leading `export `, if you have those
        # then, split name / value pair
        # key, value = line.replace('export ', '', 1).strip().split('=', 1)
        key, value = line.strip().split('=', 1)
        # os.environ[key] = value  # Load to local environ
        env_vars[key] = value # Save to a list
#Load env vars*

adminToken = env_vars["ADMIN_TOKEN"]
userID = (env_vars["USERID"] if ("USERID" in env_vars) else "5c1e728bc93ad2550c33b110")
s = requests.Session()

url = (env_vars["SERVER_URL"] if ("SERVER_URL" in env_vars) else "http://localhost:3000")+"/api/alerts/<replace>?file=remove"


def save_speech(data):
	"""
	Saves mic data to temporary WAV file. Returns filename of saved file
	"""
	filename = 'output_'+str(int(time.time()))
	# writes data to WAV file
	data = b''.join(data)
	wf = wave.open(filename + '.wav', 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()
	return filename + '.wav'

def send


while (1):
	option = int(raw_input("get(0),getId(1),postFile(2),DeleteID(3),SaveFile(4)"))
	if (option == 4):
		r = requests.get(url.replace("<replace>",raw_input("id:")))
		tmp = json.loads(r.content)
		filee = open(raw_input("output_filename:"), "wb")
		filee.write(base64.b64decode(tmp["file"]))
		filee.close()
	elif (option == 3):
		r = requests.delete(url.replace("<replace>",raw_input("id:")))
		print r.content
	elif (option == 2):
		fileName = raw_input("file name:")
		data = base64.b64encode(open(fileName, "rb").read())
		post_fields = {'content': 'bar','file':data}     # Set POST fields here 
		r = requests.post(url = url.replace("<replace>",""), data = post_fields) 
		print r.content
	elif (option == 1):
		r = requests.get(url.replace("<replace>",raw_input("id:")))
		print r.content
	else:
		r = requests.get(url.replace("<replace>","")+"&limit=1")
		print r.content