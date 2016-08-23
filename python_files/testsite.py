animales = ['perro', 'gato']

def replace_in_list(target_list, old_value, new_value):
	new_list = []
	for e in target_list:
		if e == old_value:
			new_list.append(new_value)
		else:
			new_list.append(e)
	return new_list

print replace_in_list(animales,'perro', 'lobo')


print 'chilaqxuil' in 'chilaquiles'
