import bot_functions

#current = 65
last = 91
#max = 250

letter1 = 65
letter2 = 65

while letter1 < last:
	while letter2 < last:
		search_term = chr(letter1) + chr(letter2)
		print ('Search term: ' + search_term)
		count = bot_functions.name_count(search_term)
		print (count)
		count = int(count)
		i = 1
		skip = 0
		print (search_term)
		while skip < count:
			print ('This is the ' + str(i) + 'th go round. The skip = ' + str(skip))
			json_data = bot_functions.name_search(search_term, skip)
			bot_functions.json_to_sql(json_data)
			i += 1
			skip = skip + 250
		else:
			print ('This is the last go round. The skip = ' + str(skip))
			json_data = bot_functions.name_search(search_term, skip)
			bot_functions.json_to_sql(json_data)

		letter2 += 1
	else:
		letter1 +=1
