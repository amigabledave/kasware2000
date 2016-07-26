descripciiones = ['Descripcion 1 Smash bross',
				  'Descripcion 2 Wii',
				  'Magic the gathering',
				  'smashing pumkings,']


def find_matches(lookup_string, lookup_set):

	lookup_string = lookup_string.lower()
	lookup_words =	lookup_string.split(' ')
	main_result = []
	secondary_result = []
	for e in lookup_set:
		e_low = e.lower()
		if e_low.find(lookup_string) != -1:
			main_result.append(e)
		else:
			for word in lookup_words:
				if e_low.find(word) != -1 and e not in secondary_result:
					secondary_result.append(e)

	return main_result + secondary_result


lookup_string = 'Magic wii'

print find_matches(lookup_string, descripciiones)

print str('String').lower()