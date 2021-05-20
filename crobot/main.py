import core_modules

#This program is designed to run from the current company number up to the latest company formed


# The current newest company number is stored in a file
# This command retrieves the value from a file
# And assigns it the name 'num'
num = core_modules.get_num()

# This command search for how many companies have a particular company number
# The result should onlt ever be 0 or 1
# The result is assigned to the variable 'count'
count = core_modules.get_count(num)

# The code below depends on the number of companies found by the 'get_count' function
# If zero, the user is informed that the comapny does not yet exist
# If one, the 'search' module looks for the company data associated with that particular company number
# It prints some of this data on the screen
# If a value other than zero or one is returned, an error message is displayed
#if count == '0':
#	print ('This company does not yet exist.')
#elif count == '1':
#	core_modules.search(num)
#	print ('Search succesful.')
#else:
#	print ('Error: company count has returned a value other than 0 or 1')

#By uncommenting the below you can try to diagnose the cause of errors
#print (count)

#print ('this is the json part:')
#core_modules.make_json(num)

print ('The starting company number is ' + num + '\n')
print ('This company number occurs in the database ' + count + ' time(s)')

#Use this if you want to cycle through companies:
while count == '1':
	try:
		core_modules.make_json(num)
		core_modules.increment()
		num = core_modules.get_num()
		count = core_modules.get_count(num)
		print ('The current number is ' + num)
		print ('The count is :' + count)
		print ('\n')
	except:
		print ('There was an error on ' + num + '.')
		continue
