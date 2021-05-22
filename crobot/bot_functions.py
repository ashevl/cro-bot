def get_num(num_file):
	f = open(num_file, 'r')
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

def name_search(name):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 
	'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companies?&company_name=' + name + '&company_bus_ind=C&searchType=1' + '&skip=0&max=250&htmlEnc=0', headers=headers, body=None)

	res = h.getresponse()
	json_data = json.loads(res.read())

	for item in json_data:
		assert item in json_data

		print (item['company_name'])
		short_date = str(item['company_reg_date'])[:10]
		print ('Registered on ' + short_date)
		print ('It\'s Eircode is ' + item['eircode'])

	return json_data

def make_json(num):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 
	'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companies?&company_num=' + num + '&company_bus_ind=C&searchType=1' + '&skip=0&max=5&htmlEnc=0', headers=headers, body=None)

	res = h.getresponse()
	json_data = json.loads(res.read())

	for item in json_data:
		assert item in json_data

	with open('json_files/' + str(num) + '.txt', 'w') as outfile:
		json.dump(json_data, outfile)
	outfile.close()

def increment(num_file):
	# opens the file which has the newst company number
	f = open(num_file, 'r')

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
	f = open(num_file, 'w')
	f.write(string3)
	f.close

def read_json(num):
	import json

	f = open('json_files/' + num + '.txt', 'r')
	json_data = json.loads(f.read())

	return json_data

def json_to_text(num):
	import json

	f = open('json_files/' + num + '.txt', 'r')
	json_data = json.loads(f.read())

	for item in json_data:
		assert item in json_data

	if item['eircode'] == '':
		address = item['company_addr_1'] + ', ' + item['company_addr_2'] + ', ' + item['company_addr_3'] + ', ' + item['company_addr_4']
	else:
		address = item['eircode']

	address = address.replace(' ', '%20')
	short_date = str(item['company_reg_date'])[:10]

	f = open('tweet_files/' + num + '_tweet.txt', 'w')
	f.write(item['company_name'] + '.\n')
	f.write('Company Number: ' + str(item['company_num']) + '.\n')
	f.write('Registered on ' + short_date + '.\n')
	f.write('Find it here: maps.google.ie/?q=' + address)
	f.close()

def text_to_tweet(num):
	from twitter import tweet

	f = open('tweet_files/' + num + '_tweet.txt', 'r')
	tweet(f.read())
	f.close
