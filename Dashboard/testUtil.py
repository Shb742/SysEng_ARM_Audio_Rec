import requests,json,base64

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

adminToken = env_vars["DASHBOARD_ADMIN_TOKEN"]
url = (env_vars["DASHBOARD_URL"] if ("DASHBOARD_URL" in env_vars) else "http://localhost:3000")
api = "/api/alerts/<replace>?file=remove&token="+adminToken

while (1):
	option = int(raw_input("get(0),getId(1),postFile(2),DeleteID(3),SaveFile(4),getUsers(5),SingUp(6),Login(7),DeleteUser(8)"))
	if (option == 8):
		 r = requests.delete(url = url+"/delete/"+raw_input("id:")+"?token="+adminToken, verify=False)
		 print(r.content)
	elif (option == 7):
		 post_fields = {'username': 'test','password':'test@test'}     # Set POST fields here 
		 session = requests.Session();
		 r = session.post(url = url+"/login?&token="+adminToken, data = post_fields, verify=False) 
		 print(r.content)
		 print(session.cookies.get_dict())
	elif (option == 6):
		with requests.session() as s:
			# post to the signup form
			post_fields = {'username': 'test','password':'test@test', 'authlevel':1}     # Set POST fields here 
			username = raw_input("username :")
			password = raw_input("password :")
			authlevel = int(raw_input("authlevel :"))
			if  ((len(username)+len(password))>6):
				post_fields["username"] = username
				post_fields["password"] = password
				post_fields["authlevel"] = authlevel
			r = s.post(url+"/signup?token="+adminToken, data=post_fields, verify=False)
			print(r.content)
			print(r.cookies)
	elif (option == 5):
		r = requests.get(url+"/listusers?token="+adminToken, verify=False)
		print(r.content)
	elif (option == 4):
		print (url+api).replace("<replace>",raw_input("id:")).replace("file=remove","")
		r = requests.get( (url+api).replace("<replace>",raw_input("id:")).replace("file=remove",""), verify=False)
		tmp = json.loads(r.content)
		filee = open(raw_input("output_filename:"), "wb")
		filee.write(base64.b64decode(tmp["file"]))
		filee.close()
	elif (option == 3):
		r = requests.delete((url+api).replace("<replace>",raw_input("id:")), verify=False)
		print(r.content)
	elif (option == 2):
		fileName = raw_input("file name:")
		data = base64.b64encode(open(fileName, "rb").read())
		post_fields = {'content': raw_input("interpretted_text:"),'file':data}     # Set POST fields here
		r = requests.post(url = (url+api).replace("<replace>",""), data = post_fields, verify=False) 
		print(r.content)
	elif (option == 1):
		r = requests.get((url+api).replace("<replace>",raw_input("id:")), verify=False)
		print(r.content)
	else:
		r = requests.get((url+api).replace("<replace>","")+"&limit=5", verify=False)
		print(r.content)
