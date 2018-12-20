import requests
url = "http://localhost:3000/api/alerts/"


while (1):
	option = int(raw_input("get(0),getId(1),postFile(2),DeleteID(3)"))
	if (option == 3):
		r = requests.delete(url+raw_input("id:"))
		print r.content
	elif (option == 2):
		fileName = raw_input("file name:")
		data = open(fileName, "rb").read()
		post_fields = {'content': 'bar','file':data}     # Set POST fields here 
		r = requests.post(url = url, data = post_fields) 
		print r.content
	elif (option == 1):
		r = requests.get(url+raw_input("id:"))
		print r.content
	else:
		r = requests.get(url+"?limit=1")
		print r.content