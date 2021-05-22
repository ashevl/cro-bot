import bot_functions

# This module finds and posts data on one company at a time

# Gets the most recently searched company number
num_file = 'corp_num.txt'
num = bot_functions.get_num(num_file)

# Find the number of matches for the current company number on cro.ie
# The result should only ever be 0 or 1
count = bot_functions.get_count(num)

print ('The starting company number is ' + num)
print ('This company number occurs in the database ' + count + ' time(s)\n')

# Pulls data on the current company from cro.ie and saves it as a json file
# The json file is then converted to text file containing the contents of the tweet
# The json file is also used to make a tect file with the company address
# the Google Maps API is then used to make the address into a 'geocode' and save to a file
# The contents of the text file are then posted to twitter
# And the next +1 company number is saved to a text file
if count == '1':
	bot_functions.make_json(num)
	bot_functions.json_to_text(num)
	bot_functions.json_to_address(num)
	bot_functions.address_to_geocode(num)
	bot_functions.text_to_tweet(num)
	bot_functions.increment(num_file)
else:
	print ('That\'s all for now.')

print ('\nThe current number is ' + num)
print ('The count is :' + count)
