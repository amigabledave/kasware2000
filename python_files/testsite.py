from datetime import datetime, timedelta, time

days = 0
months = 0
years = 0



d_repeats_on = {
	'repeats_on_Mon': False,
	'repeats_on_Tue': False, 
	'repeats_on_Wed': False, 
	'repeats_on_Thu': False,
	'repeats_on_Fri': False,
	'repeats_on_Sat': False,
	'repeats_on_Sun': False}


d_repeats = {'R000':'Never',
			 'R001':'Daily',
			 'R007':'Weekly',
			 'R030':'Monthly',
			 'R365':'Yearly'}


d_repeats = {'R000':'Never',
			 'R001':1,
			 'R007':7,
			 'R030':30,
			 'R365':365}


l_repeats_on = [0,0,0,0,0,0,0] # Monday = 0, Sunday = 6 on datetime.today().weekday()


print datetime.today() + timedelta(days=2)
print datetime.today().weekday()



def determine_days_for_next_weekly_repeats_on(l_repeats_on):
	days = 0
	return

def find_next_1(l_repeats_on):
	active_position = datetime.today().weekday()
	return

abc = ['a', 'b', 'c', 'd', 'e', 'f']

def reorginize_list(l, position):
	result = []
	list_size = len(l)
	active_position = position
	for i in range(0, list_size):
		result.append(l[active_position]) 
		active_position += 1
		if active_position >= list_size:
			active_position = 0
	return result

print reorginize_list(abc, 4)











#-------------------
# import math

# kpts_goals_parameters = {
# 	'typical_week_effort_distribution':[1, 1, 1, 1, 1, 0.5, 0],
# 	'yearly_vacations_day': 12,
# 	'yearly_shit_happens_days': 6,
# 	'minimum_daily_hours_of_fully_focus_effort':7}


# def calculate_user_kpts_goals(kpts_goals_parameters):

# 	yearly_vacations_day = kpts_goals_parameters['yearly_vacations_day']
# 	yearly_shit_happens_days = kpts_goals_parameters['yearly_shit_happens_days']
# 	minimum_daily_hours_of_fully_focus_effort = kpts_goals_parameters['minimum_daily_hours_of_fully_focus_effort']
	
# 	typical_week_effort_distribution = kpts_goals_parameters['typical_week_effort_distribution']
# 	typical_week_active_days = sum(typical_week_effort_distribution)

# 	typical_day_minimum_effort = minimum_daily_hours_of_fully_focus_effort*60*3

# 	typical_week_minimum_effort = typical_day_minimum_effort*typical_week_active_days

# 	active_days = 365.25 - (yearly_vacations_day + yearly_shit_happens_days) - ((7 - typical_week_active_days) * (365.25/7.0))

# 	yearly_effort_goal = active_days * typical_day_minimum_effort

# 	daily_effort_consumption = yearly_effort_goal/365.25

# 	typical_weekly_goals = []
# 	for e in typical_week_effort_distribution:
# 		typical_weekly_goals.append(e * typical_day_minimum_effort)

# 	user_kpts_goals = {
# 		'typical_day_minimum_effort': math.ceil(typical_day_minimum_effort),
# 		'typical_week_minimum_effort': math.ceil(typical_week_minimum_effort),
# 		'daily_effort_consumption': math.ceil(daily_effort_consumption),
# 		'typical_weekly_goals': typical_weekly_goals
# 	}

# 	return user_kpts_goals
# print calculate_user_kpts_goals(kpts_goals_parameters)


#-------------------
# from datetime import datetime, timedelta, time

# today = datetime.today()
# time = today.time()
# hours = time.hour + time.minute/60.0 + time.second/3600.0 
# timedelta = timedelta(hours=hours)
# # timedelta = timedelta(hours=(time.hour + time.minute/60.0))

# print today
# print time
# print today - timedelta
# print today.toordinal() * 10
# print(today + timedelta).toordinal()
# print hours



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