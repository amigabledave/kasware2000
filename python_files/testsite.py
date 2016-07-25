
import math, random
from datetime import datetime, timedelta, time

today = datetime.today()

user_start_time = '13:00'

day_start_time = datetime.strptime(user_start_time, '%H:%M').time()
user_start_hour = day_start_time.hour + day_start_time.minute/60.0 

active_date_date = (datetime.today() - timedelta(hours=user_start_hour))
active_date = (datetime.today() - timedelta(hours=user_start_hour)).toordinal() 

past_date = active_date - 30
past_date_date = datetime.fromordinal(past_date)

kpts_weekly_goals = [28.0, 28.0, 28.0, 28.0, 28.0, 14.0, 0.0]

print today
print today.toordinal()
print
print active_date_date
print active_date


class DailyLog():

	goal_achieved = False

	streak_start_date = active_date #An number that represents a date
	Streak = 0
	Goal = 0
	
	EffortReserve = 0
	PointsToGoal = 0
	
	SmartEffort = 0
	Stupidity = 0



active_log = DailyLog()
active_log.user_date_date = active_date_date
active_log.user_date = active_date
active_log.PointsToGoal = 25

last_log = DailyLog()
last_log.user_date_date = past_date_date
last_log.user_date = past_date
last_log.EffortReserve = 200
last_log.streak_start_date = past_date



class Event():

	user_date = active_date_date	
	user_date = active_date
	
	kpts_type = ''
	score = 0

class Theory():
 	day_start_time = datetime.strptime('06:00', '%H:%M').time()
 	kpts_goals = {'typical_day_minimum_effort': 28.0, 'kpts_weekly_goals': [28.0, 28.0, 28.0, 28.0, 28.0, 14.0, 0.0], 'active_days': 269.0}
	last_DailyLog = past_date
theory = Theory()

def generate_random_events(n):
	result = []
	for i in range(0,n):
		new_event = Event()
		new_event.kpts_type = random.choice(['SmartEffort', 'SmartEffort', 'Stupidity'])
		new_event.score = random.randrange(1, 5)
		result.append(new_event)
	return result
random_events = generate_random_events(50)
def update_active_log(active_log, event):
	# def update_active_log(self, event):
	# 	active_log = self.active_log

	PointsToGoal = active_log.PointsToGoal

	if event.kpts_type == 'SmartEffort':
		active_log.SmartEffort += event.score
		PointsToGoal -= event.score

	if event.kpts_type == 'Stupidity':
		active_log.Stupidity += event.score
		PointsToGoal += event.score

	if not active_log.goal_achieved:
		if PointsToGoal <= 0:
			active_log.goal_achieved = True
			active_log.Streak += 1
			active_log.EffortReserve -= PointsToGoal
			active_log.PointsToGoal = 0
		else:
			active_log.PointsToGoal = PointsToGoal

	else:
		active_log.EffortReserve -= PointsToGoal

	# active_log.put()
	return active_log

def update_active_log_with_random_events(active_log, random_events):
	
	for event in random_events:
		print 'PointsToGoal: ',active_log.PointsToGoal, 'EffortReserve: ', active_log.EffortReserve, 'SmartEffort: ', active_log.SmartEffort, 'Stupidity: ', active_log.Stupidity		
		print 'Kpts Type: ', event.kpts_type, 'Score: ', event.score
		print
		update_active_log(active_log, event)
	print
	print 'PointsToGoal: ',active_log.PointsToGoal, 'EffortReserve: ', active_log.EffortReserve, 'SmartEffort: ', active_log.SmartEffort, 'Stupidity: ', active_log.Stupidity
	print
	print
	print 'Goal achieved:', active_log.goal_achieved, 'Streak:', active_log.Streak
# update_active_log_with_random_events(active_log, random_events)


# def get_active_log(self):
# 	theory = self.theory
def get_active_log(theory):
	
	day_start_time = theory.day_start_time
	user_start_hour = day_start_time.hour + day_start_time.minute/60.0 

	active_date = (datetime.today()-timedelta(hours=user_start_hour)).toordinal() 
	last_DailyLog = theory.last_DailyLog
	
	if last_DailyLog == active_date:
		active_log = DailyLog 
		# user_key = theory.key
		# active_log = DailyLog.query(DailyLog.theory == user_key ).filter(DailyLog.user_date == active_date).fetch()[0]
		# active_log = active_log[0]

	else:
		active_log = fill_log_gaps(self, last_DailyLog)

	return active_log



def fill_one_log_gap(theory, last_log, kpts_weekly_goals):

	user_date = last_log.user_date + 1
	user_date_date = datetime.fromordinal(user_date)

	active_weekday = (user_date_date).weekday()
	Goal = int(kpts_weekly_goals[active_weekday])

	old_EffortReserve = last_log.EffortReserve

	if old_EffortReserve - Goal >= 0:
		goal_achieved = True
		streak_start_date = last_log.streak_start_date

		Streak = last_log.Streak + 1
		EffortReserve = old_EffortReserve - Goal
		PointsToGoal = 0 

	else:
		goal_achieved = False
		streak_start_date = user_date

		Streak = 0
		EffortReserve = 0
		PointsToGoal = Goal - old_EffortReserve


	new_log = DailyLog()
		
	new_log.user_date_date = user_date_date
	new_log.user_date = user_date

	new_log.goal_achieved = goal_achieved
	new_log.streak_start_date = streak_start_date

	new_log.Streak = Streak
	new_log.Goal = Goal
	new_log.EffortReserve = EffortReserve
	new_log.PointsToGoal = PointsToGoal
	

	# new_log = DailyLog(
	# 	theory = theory.key,
		
	# 	user_date_date = user_date_date,
	# 	user_date = user_date,

	# 	goal_achieved = goal_achieved,
	# 	streak_start_date = streak_start_date,

	# 	Streak = Streak,
	# 	Goal = Goal,
	# 	EffortReserve = EffortReserve,
	# 	PointsToGoal = PointsToGoal)
	# new_log.put()
	return new_log
# new_log = fill_one_log_gap(theory, last_log, kpts_weekly_goals)
# print last_log.user_date_date, last_log.user_date, last_log.EffortReserve, last_log.Streak
# print new_log.user_date_date, new_log.user_date, new_log.EffortReserve, new_log.Streak
# new_log = fill_one_log_gap(theory, new_log, kpts_weekly_goals)
# print new_log.user_date_date, new_log.user_date, new_log.EffortReserve, new_log.Streak, new_log.streak_start_date



# def find_latest_log(log_set):
# 	latest_date = 0
# 	for log in log_set:
# 		if log.user_date > latest_date:
# 			latest_log = log
# 			latest_date = latest_log.user_date
# 	return latest_log
# def find_log(log_set, active_date):
# 	for log in log_set:
# 		if log.user_date == active_date:
# 			return log
def fill_log_gaps(theory, active_date):

	kpts_weekly_goals = theory.kpts_goals['kpts_weekly_goals']

	# latest_log = find_latest_log(log_set, active_date)
	latest_log = last_log
	latest_log_date = latest_log.user_date

	while latest_log_date < active_date:
		print latest_log.user_date_date, latest_log.user_date, latest_log.EffortReserve, latest_log.Streak, latest_log.streak_start_date
		latest_log = fill_one_log_gap(theory, latest_log, kpts_weekly_goals)
		latest_log_date = latest_log.user_date

	print latest_log.user_date_date, latest_log.user_date, latest_log.EffortReserve, latest_log.Streak, latest_log.streak_start_date
	return latest_log

fill_log_gaps(theory, active_date)








