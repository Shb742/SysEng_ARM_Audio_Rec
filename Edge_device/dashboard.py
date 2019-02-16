import requests,json,base64,time
import wave,io
import threading

#Disable warning about https certificates
try:
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except Exception:
	pass


#Load env vars
env_vars = {}
with open(".env") as env_file:
	for line in env_file:
		if line.startswith('#'):
			continue
		key, value = line.strip().split('=', 1)
		env_vars[key] = value
#Load env vars*

userName = (env_vars["USERNAME"] if ("USERNAME" in env_vars) else "test")
password = (env_vars["PASSWORD"] if ("PASSWORD" in env_vars) else "test@test")
location = (env_vars["LOCATION"] if ("LOCATION" in env_vars) else "UNKWN")

session = requests.Session()
url = (env_vars["SERVER_URL"] if ("SERVER_URL" in env_vars) else "https://localhost")
last_login = 0

channels = 1
sample_rate = 16000
sample_width = 2
# lock to serialize console output
lock = threading.Lock()


def encode_speech(data):
	#globals
	global channels
	global sample_rate
	global sample_width
	#globals*
	data = data[:11796400]#Save Only first ~15Mb(once base64 encoded)
	buf = io.BytesIO()
	wf = wave.open(buf, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(sample_width)
	wf.setframerate(sample_rate) 
	wf.writeframes(data)
	wf.close()
	buf.seek(0)
	return base64.b64encode(buf.read()).decode()


def login(force=False):
	#globals
	global userName
	global password
	global session
	global url
	global last_login
	#globals*
	if (force or ((time.time()-last_login) > 1800.0) ):# if last login was more than 30 mins ago login again
		post_fields = {'username': userName,'password':password}   
		try:
			r = session.post(url = url+"/login", data = post_fields, verify=False, timeout=10)
			print("logged in")
			last_login = time.time()
		except:
			pass#Fail silently

def ping():
	#globals
	global session
	global url
	global lock
	#globals*
	while 1:
		with lock:
			login()
			try:
				print("pinging.....")
				r = session.get(url = url+"/ping", verify=False, timeout=10)
				resp = r.content.decode("utf-8") 
				print("here")
				print(resp)
				if (not('Success' in json.loads(resp))):
					print("ping-retrying...")
					login(True)
					r = session.get(url = url+"/ping", verify=False, timeout=10)
			except:
				pass#Fail silently
		time.sleep(300)#ping every 5 mins

def send(data,text):
	#globals
	global session
	global url
	global location
	global lock
	#globals*
	with lock:
		login()
		text = ' '.join(text).replace("<s>","").replace("</s>","").replace("<","").replace(">","")
		post_fields = {'content': text ,'file':encode_speech(data),'type':'data:audio/wav;base64,', 'location':location}     # Set POST fields here
		try:
			r = session.post(url = url+"/api/alerts/?file=remove", data = post_fields, verify=False, timeout=100) 
			#Retry one time if post failed (i.e session destroyed)
			if (not('Success' in json.loads(r.content.decode("utf-8")))):
				print("retrying.....")
				login(True)
				r = session.post(url = url+"/api/alerts/?file=remove", data = post_fields, verify=False, timeout=100) 
			#Retry one time if post failed (i.e session destroyed)*
			print(r.content)
		except:
			pass#Fail silently
	