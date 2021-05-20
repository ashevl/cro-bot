def get_num():
	f = open('corp_num.txt', 'r')
	num = f.read()
	return num

def get_count(num):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companycount?&company_num=' + num + '&company_bus_ind=C&searchType=1', headers=headers, body=None)

	res = h.getresponse()
	count = (res.read()).decode()
	return count

def search(num):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 
	'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companies?&company_num=' + num + '&skip=0&max=5&htmlEnc=0', headers=headers, body=None)

	res = h.getresponse()
	json_data = json.loads(res.read())

	for item in json_data:
		assert item in json_data

		print (item['company_name'])
		short_date = str(item['company_reg_date'])[:10]
		print ('Registered on ' + short_date)
		print ('It\'s Eircode is ' + item['eircode'])

def make_json(num):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 
	'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companies?&company_num=' + num + '&skip=0&max=5&htmlEnc=0', headers=headers, body=None)

	res = h.getresponse()
	json_data = json.loads(res.read())

	for item in json_data:
		assert item in json_data

	with open('json_files/' + str(num) + '.txt', 'w') as outfile:
		json.dump(json_data, outfile)
	outfile.close()

def increment():
	# opens the file which has the newst company number
	f = open('corp_num.txt', 'r')

	# assigna the contents of this text file the name 'string1'
	string1 = f.read()

	# strips out any new line characters
	string2 = string1.rstrip('\n')

	# converts the string into an integer
	num = int(string2)

	# adds one
	num += 1

	# converts the new integer back into a string
	string3 = str(num)

	# write the new value to the file
	f = open('corp_num.txt', 'w')
	f.write(string3)
	f.close

def read_json(num):
	import json

	f = open('json_files/' + num + '.txt', 'r')
	json_data = json.loads(f.read())

	return json_data
