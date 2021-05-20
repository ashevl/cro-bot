import core_modules
from twitter import tweet

# The current newest company number is stored in a file
# This command retrieves the value from a file
# And assigns it the name 'num'
num = core_modules.get_num()

# This command searches for how many companies have a particular company number
# The result should onlt ever be 0 or 1
# The result is assigned to the variable 'count'
count = core_modules.get_count(num)

print ('The starting company number is ' + num)
print ('This company number occurs in the database ' + count + ' time(s)\n')

#Version for when using cron
core_modules.make_json(num)

if count == '1':
	json_data = core_modules.read_json(num)
	for item in json_data:
		assert item in json_data

	short_date = str(item['company_reg_date'])[:10]
	print (item['company_name'])

	if item['eircode'] == '':
		address = item['company_addr_1'] + item['company_addr_2'] + item['company_addr_3'] + item['company_addr_4']
	else:
		address = item['eircode']

	address = address.replace(' ', '%20')

	f = open('tweet_files/' + num + '_tweet.txt', 'a')
	f.write(item['company_name'] + '.\n')
	f.write('Company Number: ' + str(item['company_num']) + '.\n')
	f.write('Registered on ' + short_date + '.\n')
	f.write('Find it here: maps.google.ie/?q=' + address)
	f.close()

	f = open('tweet_files/' + num + '_tweet.txt', 'r')
	tweet(f.read())
	f.close
	core_modules.increment()
else:
	print ('That\'s all for now')

print ('The current number is ' + num)
print ('The count is :' + count)
