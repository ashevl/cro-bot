def get_num(num_file):
	f = open(num_file, 'r')
	num = f.read()
	f.close()
	return num

def num_count(num):
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

def name_count(name):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companycount?&company_name=' + name + '&company_bus_ind=C&searchType=2', headers=headers, body=None)

	res = h.getresponse()
	count = (res.read()).decode()
	return count

def name_search(name, skip):
	import http.client, json
	from auth import (
		cro_user,
		cro_key
	)

	skip = str(skip)

	h = http.client.HTTPSConnection('services.cro.ie') 

	headers = {'User-Agent': cro_user, 'Host': 'services.cro.ie', 'Content-type': 
	'application/json', 'Authorization': cro_key }

	h.request('GET', '/cws/companies?&company_name=' + name + '&company_bus_ind=C&searchType=2' + '&skip=' + skip + '&max=250&htmlEnc=1', headers=headers, body=None)

	res = h.getresponse()
	json_data = json.loads(res.read())
	for item in json_data:
		assert item in json_data
#		print (item['company_name'])

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

def deincrement(num_file):
	# opens the file which has the newst company number
	f = open(num_file, 'r')

	# assigna the contents of this text file the name 'string1'
	string1 = f.read()

	# strips out any new line characters
	string2 = string1.rstrip('\n')

	# converts the string into an integer
	num = int(string2)

	# subtracts one
	num -= 1

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

def json_to_address(num):
	import json

	f = open('json_files/' + num + '.txt', 'r')
	json_data = json.loads(f.read())

	for item in json_data:
		assert item in json_data

	if item['eircode'] == '':
		address = item['company_addr_1'] + ', ' + item['company_addr_2'] + ', ' + item['company_addr_3'] + ', ' + item['company_addr_4'] + ', Ireland'
	else:
		address = item['eircode'] + ',Ireland'

	f = open('address_files/' + num + '_address.txt', 'w')
	f.write(address)
	f.close()

def address_to_geocode(num):
	import googlemaps, json
	from auth import maps_key

	address_file = open('address_files/' + num + '_address.txt', 'r')
	address = address_file.read()
	print (address)
	gmaps = googlemaps.Client(key=maps_key)
	geocode_result = gmaps.geocode(address)

	for item in geocode_result:
		assert item in geocode_result

	with open('geocode_files/' + num + '_geocode.txt', 'w') as outfile:
		json.dump(geocode_result, outfile)
	outfile.close()
	return geocode_result

def make_db():

	import sqlite3

	connection = sqlite3.connect("database_files/crobot.db")
	cursor = connection.cursor()

	sql_command = """
	CREATE TABLE companies (
		company_num int PRIMARY KEY, 
		company_bus_ind	varchar(1),
		company_name varchar(200),
		company_addr_1 varchar(800),
		company_addr_2	varchar(800),
		company_addr_3	varchar(800),
		company_addr_4	varchar(800),
		company_reg_date varchar(20),
		company_status_desc varchar(100),
		company_status_date varchar(20),
		last_ar_date varchar(20),
		next_ar_date varchar(20),
		last_acc_date varchar(20),
		comp_type_desc varchar(100),
		company_type_code int,
		company_status_code int,
		place_of_business varchar(50),
		eircode	varchar(20)
	);"""

	cursor.execute(sql_command)

	connection.commit()
	connection.close()

def json_to_sql(json_data):
	import json, sqlite3

	connection = sqlite3.connect("database_files/crobot.db")
	cursor = connection.cursor()

	for item in json_data:
		assert item in json_data

		company_name = item['company_name']
		company_addr_1 = item['company_addr_1']
		company_addr_2 = item['company_addr_2']
		company_addr_3 = item['company_addr_3']
		company_addr_4 = item['company_addr_4']
		place_of_business = item['place_of_business']

		format_str = """INSERT OR REPLACE INTO companies (company_num, company_bus_ind, company_name, company_addr_1, company_addr_2, 
		company_addr_3, company_addr_4, company_reg_date, company_status_desc, company_status_date, last_ar_date, next_ar_date, 
		last_acc_date , comp_type_desc, company_type_code, company_status_code, place_of_business, eircode) VALUES ("{company_num}", 
		"{company_bus_ind}", "{company_name}", "{company_addr_1}", "{company_addr_2}", "{company_addr_3}", "{company_addr_4}", 
		"{company_reg_date}", "{company_status_desc}", "{company_status_date}", "{last_ar_date}", "{next_ar_date}", "{last_acc_date}", 
		"{comp_type_desc}", "{company_type_code}", "{company_status_code}", "{place_of_business}", "{eircode}");"""

		sql_command = format_str.format(company_num = item['company_num'],company_bus_ind = item['company_bus_ind'], company_name = 
		company_name, company_addr_1 = company_addr_1, company_addr_2 = company_addr_2, company_addr_3 = company_addr_3, company_addr_4 = 
		company_addr_4, company_reg_date = item['company_reg_date'], company_status_desc = item['company_status_desc'], company_status_date 
		= item['company_status_date'], last_ar_date = item['last_ar_date'], next_ar_date = item['next_ar_date'], last_acc_date = 
		item['last_acc_date'], comp_type_desc = item['comp_type_desc'], company_type_code = item['company_type_code'], company_status_code = 
		item['company_status_code'], place_of_business = place_of_business, eircode = item['eircode'])

		print (company_name)
		cursor.execute(sql_command)

	connection.commit()
	connection.close()

def search_paramters():

	first = '48'
	last = '90'

def json_to_mysql(json_data):
	import json
	import mariadb

	mydb = mariadb.connect(
	  host="localhost",
	  user="andrew",
	  password="",
	  database="crobot"
	)

	mycursor = mydb.cursor()

	for item in json_data:
		assert item in json_data

		sql = """REPLACE INTO companies (company_num,
			company_bus_ind,
			company_name,
			company_addr_1,
			company_addr_2,
			company_addr_3,
			company_addr_4,
			company_reg_date,
			company_status_desc,
			company_status_date,
			last_ar_date,
			next_ar_date,
			last_acc_date,
			comp_type_desc,
			company_type_code,
			company_status_code,
			place_of_business,
			eircode)

			VALUES (%d,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%s,
			%d,
			%d,
			%s,
			%s)"""

		val = (	item['company_num'],
			item['company_bus_ind'],
			item['company_name'],
			item['company_addr_1'],
			item['company_addr_2'],
			item['company_addr_3'],
			item['company_addr_4'],
			item['company_reg_date'],
			item['company_status_desc'],
			item['company_status_date'],
			item['last_ar_date'],
			item['next_ar_date'],
			item['last_acc_date'],
			item['comp_type_desc'],
			item['company_type_code'],
			item['company_status_code'],
			item['place_of_business'],
			item['eircode']
		)
		mycursor.execute(sql, val)

	mydb.commit()
	mydb.close()

	print(mycursor.rowcount, "record inserted.")
