import bot_functions

#This program is designed to run from the current company number up to the latest company formed

# The current company number is stored in a file
# This command retrieves the value from a file
# And assigns it the name 'num'
num_file = 'cycle_num.txt'
num = bot_functions.get_num(num_file)

# This command search for how many companies have a particular company number
# The result should onlt ever be 0 or 1
# The result is assigned to the variable 'count'
count = bot_functions.num_count(num)

#By uncommenting the below you can try to diagnose the cause of errors
#print (count)

print ('The starting company number is ' + num + '\n')
print ('This company number occurs in the database ' + count + ' time(s)')

#Use this if you want to cycle through companies:
i = 1
while count == '1':
#	try:
	bot_functions.make_json(num)
	bot_functions.json_to_address(num)
#	bot_functions.address_to_geocode(num)
	json_data = bot_functions.read_json(num)
	bot_functions.json_to_mysql(json_data)
	bot_functions.increment(num_file)
	i = i + 1
	num = bot_functions.get_num(num_file)
	count = bot_functions.num_count(num)
	print ('The current number is ' + num)
	print ('The count is :' + count + '\n')
	print ('The search has been performed ' + str(i) + ' times.\n')
#	except:
#		print ('There was an error on ' + num + '.')
#		bot_functions.increment(num_file)
#		continue
