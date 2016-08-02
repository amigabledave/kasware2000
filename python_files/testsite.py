# -*- coding: utf-8 -*-
def remplaza_acentos(palabra):
	
	letras_a_remplazar =[
		['Á','A'],
		['á','a'],
		['É','E'],
		['é','e'],
		['Í','I'],
		['í','i'],
		['Ó','O'],
		['ó','o'],
		['Ú','U'],
		['ú','u'],
		['Ñ','N'],
		['ñ','n'],
	]
	palabra = palabra.decode('utf-8')
	for letra in letras_a_remplazar:
		palabra = palabra.replace(letra[0].decode('utf-8'),letra[1])

	return palabra


def prepare_tags_for_saving(tags_string):

	tags_string = remplaza_acentos(tags_string)
	valid_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','_',',']
	clean_tags_string = ''
	for i in range(0,len(tags_string)):
		character = tags_string[i]
		if character in valid_characters:
			clean_tags_string += character
	tags = clean_tags_string.split(',')
	final_tags_string = ''
	i = len(tags)
	for tag in tags:
		i -= 1
		final_tags_string += tag
		if i > 0:
			final_tags_string += ', '

	return final_tags_string, tags




print prepare_tags_for_saving('')