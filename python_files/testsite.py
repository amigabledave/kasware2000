from datetime import datetime, timedelta, time

today = datetime.today()
time = today.time()
hours = time.hour + time.minute/60.0 + time.second/3600.0 
timedelta = timedelta(hours=hours)
# timedelta = timedelta(hours=(time.hour + time.minute/60.0))

print today
print time
print time.microsecond/3600000000.0000000000
print today - timedelta

print today.toordinal() * 10
print(today + timedelta).toordinal()

print
print
print hours



#-------------------
# def determine_return_to():
# 	url_kasware = 'http://kasware.com'
# 	url_activo = 'http://kasware.com/TodaysMission'

# 	if url_activo.find(url_kasware) != -1:
# 		return url_activo[len(url_kasware):]
# 	else:
# 		return '/'
# print determine_return_to()

#-----------
# def gatificar(funcion):
# 		def inner(*args, **kwarg):
# 			return funcion(*args, **kwarg) + ' miau miau'
# 		return inner


# @gatificar
# def perrito(x): 
# 	return x + ' guau guau'

# print perrito('dartagnan')

# perrito = gatificar(perrito)
# print perrito('dartagnan')

# def funcion_basica():
# 	for i in range(0,10):
# 			print i

# diccionario = {
# 	'ejecuta_funcion': funcion_basica()
# }


# print diccionario['ejecuta_funcion']	



#----------
# Checar si en efecto estaba linkeado bien un KSU con su teoria correspondiente
# ksu_theoryID = 'ag9kZXZ-a2Fzd2FyZTIwMDByEwsSBlRoZW9yeRiAgICAgICACww'
# theory_key = 'ag9kZXZ-a2Fzd2FyZTIwMDByEwsSBlRoZW9yeRiAgICAgICACww'
# print ksu_theoryID == theory_key


#----------
# Syntaxis para checar si se cumplen dos condiciones y nombrar una variable al mismo tiempo
# x = True
# y = 'Valor de y'
# z = x and y
# print z