# -*- coding: utf-8 -*-

acentos = 'un Únicornio iba corriendo ñinos saltandos íiiii jejeje ó'

# print acentos.decode('utf-8').lower()

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

	for letra in letras_a_remplazar:
		palabra = palabra.replace(letra[0],letra[1])

	return palabra		

print remplaza_acentos(acentos)