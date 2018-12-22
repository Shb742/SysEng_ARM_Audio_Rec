import requests,json,base64,time
import wave,io,pyaudio


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

userName = (env_vars["USERNAME"] if ("USERNAME" in env_vars) else "test")
password = (env_vars["PASSWORD"] if ("PASSWORD" in env_vars) else "test@test")
location = (env_vars["LOCATION"] if ("LOCATION" in env_vars) else "UNKWN")

session = requests.Session()
url = (env_vars["SERVER_URL"] if ("SERVER_URL" in env_vars) else "http://localhost:3000")
last_login = 0

channels = 1
sample_rate = 16000


def encode_speech(data):
	#globals
	global channels
	global sample_rate
	#globals*
	data = b''.join(data)[:11796400]#Save Only first ~15Mb(once base64 encoded)
	buf = io.BytesIO()
	wf = wave.open(buf, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()
	buf.seek(0)
	return base64.b64encode(buf.read()).decode()


def login():
	#globals
	global userName
	global password
	global session
	global url
	global last_login
	#globals*
	if ( (time.time()-last_login) > 1800.0):# if last login was more than 30 mins ago login again
		post_fields = {'username': userName,'password':password}   
		r = session.post(url = url+"/login", data = post_fields)
		print(session.cookies.get_dict())
		last_login = time.time()

def send(data,text):
	#globals
	global userName
	global password
	global session
	global url
	global location
	#globals*
	login()
	post_fields = {'content': json.dumps(text) ,'file':encode_speech(data),'type':'data:audio/wav;base64,', 'location':location}     # Set POST fields here 
	r = session.post(url = url+"/api/alerts/?file=remove", data = post_fields) 
	print(r.content)


	

