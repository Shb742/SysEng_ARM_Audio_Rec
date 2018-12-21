import requests,json,base64
url = "http://13.73.231.131/api/alerts/"


while (1):
	option = int(raw_input("get(0),getId(1),postFile(2),DeleteID(3),SaveFile(4)"))
	if (option == 4):
		r = requests.get(url+raw_input("id:"))
		tmp = json.loads(r.content)
		filee = open(raw_input("output_filename:"), "wb")
		filee.write(base64.b64decode(''.join(chr(i) for i in tmp["file"]["data"])))
		filee.close()
	elif (option == 3):
		r = requests.delete(url+raw_input("id:"))
		print r.content
	elif (option == 2):
		fileName = raw_input("file name:")
		data = base64.b64encode(open(fileName, "rb").read())
		post_fields = {'content': 'bar','file':data}     # Set POST fields here 
		r = requests.post(url = url, data = post_fields) 
		print r.content
	elif (option == 1):
		r = requests.get(url+raw_input("id:"))
		print r.content
	else:
		r = requests.get(url+"?limit=1")
		print r.content