from datetime import datetime, timedelta, time

today = datetime.today()

d_repeats_on = {'repeats_on_Sat': False, 'repeats_on_Sun': False, 'repeats_on_Thu': True, 'repeats_on_Mon': True, 'repeats_on_Wed': False, 'repeats_on_Fri': False, 'repeats_on_Tue': False}

def d_to_l_repeats_on(d_repeats_on):
	result = []
	l_repeats_on_keys = ['repeats_on_Mon', 'repeats_on_Tue', 'repeats_on_Wed', 'repeats_on_Thu', 'repeats_on_Fri', 'repeats_on_Sat', 'repeats_on_Sun']
	for day in l_repeats_on_keys:
		result.append(d_repeats_on[day])
	return result

l_repeats_on = d_to_l_repeats_on(d_repeats_on)
print l_repeats_on


def reorginize_list(l, position):
	result = []
	list_size = len(l)
	active_position = position
	for i in range(0, list_size):		
		active_position += 1
		if active_position >= list_size:
			active_position = 0
		result.append(l[active_position]) 
	return result

active_position = today.weekday()
print
print active_position

repeats_on_list = reorginize_list(l_repeats_on, active_position)
print 
print repeats_on_list


def find_weekday(repeats_on_list):		
	i = 1
	for weekday in repeats_on_list:
		if weekday: #xx
			return i
		else:
			i += 1
	return 0

print
print find_weekday(repeats_on_list)


