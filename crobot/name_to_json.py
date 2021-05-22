import json, bot_functions

name = 'ryanair'
json_data = bot_functions.name_search(name)

with open('search_test.txt', 'w') as outfile:
	json.dump(json_data, outfile)
outfile.close
