#KASware V2.0.0 | Copyright 2016 Kasware Inc.
# -*- coding: utf-8 -*-
import webapp2, jinja2, os, re, random, string, hashlib, json, logging, math 

from datetime import datetime, timedelta, time
from google.appengine.ext import ndb
from python_files import datastore, randomUser, constants, kasware_os

quotes = constants.quotes
constants = constants.constants

Theory = datastore.Theory
KSU = datastore.KSU
Event = datastore.Event
DailyLog = datastore.DailyLog
os_ksus = kasware_os.os_ksus


template_dir = os.path.join(os.path.dirname(__file__), 'html_files')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)



#--- Decorator functions
def super_user_bouncer(funcion):
	def user_bouncer(self):
		theory = self.theory
		if theory:
			return funcion(self)
		else:
			self.redirect('/SignUpLogIn')
		# return funcion(self)
	return user_bouncer

def CreateOrEditKSU_request_handler(funcion):
	def inner(self):
		post_details = get_post_details(self)
		user_action = post_details['action_description']
		
		return_to = determine_return_to(self)

		if user_action == 'NewKSU':
			self.redirect('/KsuEditor?ksu_id=NewKSU&return_to='+return_to)
			return

		elif user_action == 'EditKSU':
			ksu_id = post_details['ksu_id']
			self.redirect('/KsuEditor?ksu_id='+ksu_id+'&return_to='+return_to)
			return

		elif user_action == 'SearchTheory': 
			lookup_string = remplaza_acentos(self.request.get('new_lookup_string'))
			# lookup_string = self.request.get('lookup_string').encode('utf-8')
			self.redirect('/SetViewer?set_name=TheoryQuery&lookup_string='+lookup_string)

		else:
			return funcion(self, user_action, post_details)

	return inner


#-- Production Handlers
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_html(self, template, **kw):
		t = jinja_env.get_template(template)
		theory = self.theory 
		active_log = self.active_log
		if theory:				
			return t.render(theory=theory, active_log=active_log, **kw)
		else:
			return t.render(**kw)

	def print_html(self, template, **kw):##
		quote =  quotes[random.randrange(0,500)]
		quote['quote'] = quote['quote'].replace("&#39;","'")
		self.write(self.render_html(template, quote=quote, **kw))

	def set_secure_cookie(self, cookie_name, cookie_value):
		cookie_secure_value = make_secure_val(cookie_value)
		self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (cookie_name, cookie_secure_value))

	def read_secure_cookie(self, cookie_name):
		cookie_secure_val = self.request.cookies.get(cookie_name)
		return cookie_secure_val and check_secure_val(cookie_secure_val)

	def login(self, theory):
		self.set_secure_cookie('theory_id', str(theory.key.id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'theory_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		theory_id = self.read_secure_cookie('theory_id')
		self.theory = theory_id and Theory.get_by_theory_id(int(theory_id)) #if the user exist, 'self.theory' will store the actual theory object
		self.active_log = self.theory and self.get_active_log()


	def get_active_log(self):
		theory = self.theory
		
		minimum_daily_effort = theory.kpts_goals['minimum_daily_effort']

		day_start_time = theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		active_date = (datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).toordinal()# TT Time Travel aqui puedo hacer creer al programa que es otro dia
		
		last_DailyLog = theory.last_DailyLog
		user_key = theory.key		

		if last_DailyLog == active_date: 
			active_log = DailyLog.query(DailyLog.theory == user_key).filter(DailyLog.user_date == active_date).fetch()
			active_log = active_log[0]

		else:
			last_log = DailyLog.query(DailyLog.theory == user_key).filter(DailyLog.user_date == last_DailyLog).fetch()
			last_log = last_log[0]
			if last_log.user_date == (active_date - 1):
				last_log = self.fix_last_log(last_log, active_date, minimum_daily_effort)
			active_log = self.fill_log_gaps(theory, last_log, active_date)

		return active_log


	def fill_log_gaps(self, theory, last_log, active_date):

		minimum_daily_effort = theory.kpts_goals['minimum_daily_effort']
		kpts_weekly_goals = theory.kpts_goals['kpts_weekly_goals']

		latest_log = last_log
		latest_log_date = latest_log.user_date

		while latest_log_date < active_date:
			print latest_log.user_date_date, latest_log.user_date, latest_log.EffortReserve, latest_log.Streak, latest_log.streak_start_date
			latest_log = self.fill_one_log_gap(theory, latest_log, active_date, kpts_weekly_goals, minimum_daily_effort)
			latest_log_date = latest_log.user_date

		print latest_log.user_date_date, latest_log.user_date, latest_log.EffortReserve, latest_log.Streak, latest_log.streak_start_date
		theory.last_DailyLog = latest_log_date
		theory.put()
		return latest_log


	def fix_last_log(self, last_log, active_date, minimum_daily_effort):

		EffortReserve = last_log.EffortReserve
		# PointsToGoal = last_log.PointsToGoal #Se vuelve irrelevante 

		if not last_log.goal_achieved:
			if EffortReserve - minimum_daily_effort >= 0:
				last_log.goal_achieved = True
				last_log.Streak = last_log.Streak + 1
				last_log.EffortReserve = EffortReserve - minimum_daily_effort
				# last_log.PointsToGoal = 0 #Se vuelve irrelevante 

			else:
				last_log.streak_start_date = active_date - 1
				last_log.Streak = 0
				last_log.EffortReserve = 0
				# last_log.PointsToGoal = last_log.PointsToGoal - last_log.EffortReserve	
			last_log.put()
		return last_log		


	def fill_one_log_gap(self, theory, last_log, active_date, kpts_weekly_goals, minimum_daily_effort): #Creo que ya no necesito kpts_weekly_goals

		old_EffortReserve = last_log.EffortReserve
		old_PointsToGoal = last_log.PointsToGoal

		user_date = last_log.user_date + 1
		user_date_date = datetime.fromordinal(user_date)

		active_weekday = (user_date_date).weekday()
		Goal = int(kpts_weekly_goals[active_weekday])

		if (Goal + old_EffortReserve) < minimum_daily_effort:
			Goal = minimum_daily_effort - old_EffortReserve

		if user_date == active_date:
			if Goal == 0:
				goal_achieved = True	
				streak_start_date = last_log.streak_start_date
				Streak = last_log.Streak + 1
				EffortReserve = old_EffortReserve - minimum_daily_effort

			else:			
				goal_achieved = False
				streak_start_date = last_log.streak_start_date

				Streak = last_log.Streak
				EffortReserve = old_EffortReserve

			PointsToGoal = Goal

		elif old_EffortReserve - minimum_daily_effort >= 0:
			goal_achieved = True
			streak_start_date = last_log.streak_start_date

			Streak = last_log.Streak + 1
			EffortReserve = old_EffortReserve - minimum_daily_effort
			PointsToGoal = Goal 

		else:
			goal_achieved = False
			streak_start_date = user_date

			Streak = 0
			EffortReserve = 0
			PointsToGoal = Goal

		new_log = DailyLog(
			theory = theory.key,
			
			user_date_date = user_date_date,
			user_date = user_date,

			goal_achieved = goal_achieved,
			streak_start_date = streak_start_date,

			Streak = Streak,
			Goal = Goal,
			EffortReserve = EffortReserve,
			PointsToGoal = PointsToGoal)
		new_log.put()
		
		return new_log


class SignUpLogIn(Handler):
	def get(self):
		self.print_html('SignUpLogIn.html')

	def post(self):
		post_details = get_post_details(self)
		user_action = post_details['action_description']

		if user_action == 'Random_SignUp':
			post_details.update(randomUser.createRandomUser()) ## Creates a random user for testing purposes
		
		if user_action == 'SignUp' or user_action == 'Random_SignUp':
			input_error = user_input_error(post_details)
			theory = Theory.get_by_email(post_details['email'])	
			
			if input_error:
				self.print_html('SignUpLogIn.html', post_details=post_details, input_error=input_error)
			
			elif theory:
				self.print_html('SignUpLogIn.html', post_details=post_details, input_error = 'That email is already register to another user!')

			else:
				password_hash = make_password_hash(post_details['email'], post_details['password'])
				
				kpts_goals_parameters = {
						'typical_week_effort_distribution':[1, 1, 1, 1, 1, 0.5, 0],
						'yearly_vacations_day': 12,
						'yearly_shit_happens_days': 6,
						'minimum_daily_effort':20}


				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					day_start_time=datetime.strptime('06:00', '%H:%M').time(),
					timezone=-4,
					kpts_goals_parameters=kpts_goals_parameters,
					kpts_goals=calculate_user_kpts_goals(kpts_goals_parameters),
					categories={'tags':[]},
					last_DailyLog = datetime.today().toordinal())

				theory.put()

				#creates the first DailyLog entry
				day_start_time = theory.day_start_time
				user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
				active_date = (datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).toordinal() 
				active_date_date = datetime.fromordinal(active_date)
				active_weekday = (datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).weekday()
				goal = int(theory.kpts_goals['kpts_weekly_goals'][active_weekday])
				
				minimum_daily_effort = int(theory.kpts_goals['minimum_daily_effort'])

				if goal < minimum_daily_effort:
					print goal < minimum_daily_effort
					goal = minimum_daily_effort

				
				active_log = DailyLog(
					theory = theory.key,
					
					user_date_date = active_date_date,
					user_date = active_date,
					streak_start_date = active_date,
					
					Goal = goal,
					PointsToGoal=goal)
				active_log.put()

				theory.last_DailyLog = active_date
				theory.put()

				#Loads OS Ksus
				for post_details in os_ksus:
					ksu = KSU(theory=theory.key)
					ksu = prepareInputForSaving(theory, ksu, post_details)
					ksu.put()

				self.login(theory)
				self.redirect('/MissionViewer?time_frame=Today')

		if user_action == 'LogIn':			
			email = self.request.get('email')
			password = self.request.get('password')
			theory = Theory.valid_login(email, password)
			if theory:
				self.login(theory)
				self.redirect('/MissionViewer?time_frame=Today')
			else:
				self.write('incorrect username or password')


class LogOut(Handler):
	def get(self):
		self.logout()
		self.redirect('/')


class Settings(Handler):

	@super_user_bouncer
	def get(self):
		theory = self.theory
		today = datetime.today()

		local_today = datetime.today()+timedelta(hours=theory.timezone)

		day_start_time = theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		user_today = local_today-timedelta(hours=user_start_hour)

		active_date = user_today.toordinal()
		
		self.print_html('Settings.html', today=today, local_today=local_today, user_today=user_today)


	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		
		if user_action == 'SaveChanges':
			theory = self.theory
			print
			print post_details
			theory.first_name = post_details['first_name'].encode('utf-8') 
			theory.last_name = post_details['last_name'].encode('utf-8')	
	 	
	 		theory.language = str(post_details['language'])
	 		
	 		if 'hide_private_ksus' in post_details:
	 			theory.hide_private_ksus = True
			else:
				theory.hide_private_ksus = False

		 	theory.timezone = int(post_details['timezone'])

			theory.day_start_time = datetime.strptime(post_details['day_start_time'][0:5], '%H:%M').time()

		 	theory.kpts_goals_parameters = {
				'typical_week_effort_distribution':[
					float(post_details['typical_week_effort_distribution_Mon']),
					float(post_details['typical_week_effort_distribution_Tue']),
					float(post_details['typical_week_effort_distribution_Wed']),
					float(post_details['typical_week_effort_distribution_Thu']),
					float(post_details['typical_week_effort_distribution_Fri']),
					float(post_details['typical_week_effort_distribution_Sat']),
					float(post_details['typical_week_effort_distribution_Sun'])],
				'yearly_vacations_day': int(post_details['yearly_vacations_day']),
				'yearly_shit_happens_days': int(post_details['yearly_shit_happens_days']),
				'minimum_daily_effort':float(post_details['minimum_daily_effort'])}
	 	
	 		
			
	 		theory.kpts_goals = calculate_user_kpts_goals(theory.kpts_goals_parameters)
			
			active_log = self.update_active_log_based_on_new_kpts_goals(theory.kpts_goals) 		
	 		theory.put()
 		self.redirect('/MissionViewer?time_frame=Today')


	def update_active_log_based_on_new_kpts_goals(self, new_kpts_goals):
		active_log = self.active_log

		new_minimum_daily_effort = new_kpts_goals['minimum_daily_effort']

		user_date = active_log.user_date
		user_date_date = datetime.fromordinal(user_date)

		active_weekday = (user_date_date).weekday()
		new_Goal = int(new_kpts_goals['kpts_weekly_goals'][active_weekday])

		if new_Goal + active_log.EffortReserve < new_minimum_daily_effort:
			new_Goal = new_minimum_daily_effort

		new_PointsToGoal = new_Goal - active_log.SmartEffort + active_log.Stupidity

		if new_PointsToGoal < 0:
			new_minimum_dayly_effort = 0

 		active_log.Goal = new_Goal
		active_log.PointsToGoal = new_PointsToGoal
						
		active_log.put()
		return 


class KsuEditor(Handler):
	
	@super_user_bouncer
	def get(self):
		ksu_id = self.request.get('ksu_id')
		if ksu_id == 'NewKSU':
			ksu = constants['default_ksu']
		else: 
			ksu = KSU.get_by_id(int(ksu_id))

		tags = self.theory.categories['tags']
		self.print_html('KsuEditor.html', ksu=ksu, constants=constants, tags=tags)

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):		
		ksu_id = self.request.get('ksu_id')
		if ksu_id == 'NewKSU':
			ksu = KSU(theory=self.theory.key)
		else: 
			ksu = KSU.get_by_id(int(ksu_id))

		return_to = determine_return_to(self)
		
		if user_action == 'SaveChanges':
			print
			print 'Estos son los detalles'
			print post_details
			print ksu
			ksu = prepareInputForSaving(self.theory, ksu, post_details) #BUG ALERT! Hice que esta funcion fuera global - veamos si esto causa issues
			update_next_event(self, user_action, post_details, ksu)
			print 'Asi queda la fecha del siguiente evento'
			print ksu.next_event
			print
			ksu.put()

		self.redirect(return_to)
		return


class Home(Handler):
	
	@super_user_bouncer
	def get(self):
		theory = self.theory
		message = 'Welcome to KASware ' + theory.first_name + ' ' + theory.last_name
		self.write(message)

			
class SetViewer(Handler):

	@super_user_bouncer
	def get(self):
		set_name = self.request.get('set_name')
		user_key = self.theory.key
		lookup_string =''

		if not set_name:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False).order(KSU.importance).order(KSU.created).fetch()
		
		elif set_name == 'TheoryQuery':
			lookup_string = self.request.get('lookup_string')
			user_theory = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.is_deleted == False).order(KSU.importance).order(KSU.created).fetch()
			ksu_set = self.search_theory(user_theory, lookup_string)
			lookup_string = 'You searched for: ' + lookup_string
		
		elif set_name == 'Graveyard':
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == True, KSU.is_deleted == False).order(KSU.importance).order(KSU.created).fetch()
		
		else:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.ksu_type == set_name).order(-KSU.is_active).order(KSU.importance).order(KSU.created)

			if self.theory.hide_private_ksus:
				ksu_set = ksu_set.filter(KSU.is_private == False)
			
			ksu_set = ksu_set.fetch()
		

		for ksu in ksu_set:
			ksu.description_rows = determine_rows(ksu.description)
			ksu.secondary_description_rows = determine_rows(ksu.secondary_description)
			ksu.comments_rows = determine_rows(ksu.comments)

		
		tags = categories = self.theory.categories['tags'] # por el quick adder
		self.print_html('SetViewer.html', ksu_set=ksu_set, constants=constants, set_name=set_name, ksu={}, tags=tags, lookup_string=lookup_string) #

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return


	def search_theory(self, user_theory, lookup_string):
		# -*- coding: utf-8 -*-
		lookup_string = lookup_string.lower()
		lookup_words =	lookup_string.split(' ')
		main_result = []
		secondary_result = []

		for ksu in user_theory:
			if not ksu.description:
				ksu.description=''
			if not ksu.secondary_description:
				ksu.secondary_description=''
			if not ksu.tags:
				ksu.tags =''
			
			ksu_description = remplaza_acentos(ksu.description).lower() + ' ' + remplaza_acentos(ksu.secondary_description).lower() + ' ' + remplaza_acentos(ksu.tags).lower()

			if ksu_description.find(lookup_string) != -1:
				main_result.append(ksu)
			else:
				for word in lookup_words:
					if ksu_description.find(word) != -1 and ksu not in secondary_result:
						secondary_result.append(ksu)

		return main_result + secondary_result


class MissionViewer(Handler):

	@super_user_bouncer
	def get(self):
		time_frame = self.request.get('time_frame')

		tags = self.theory.categories['tags']

		todays_questions_now, todays_questions_latter, reactive_mission, today, full_mission = self.generate_todays_mission(time_frame)

		ksu_sets = []
		horizons_values = {}
		horizons_titles = {}

		if time_frame == 'Today':
			time_frame_sets = ['today']
		else:
			time_frame_sets = ['tomorrow', 'this_week', 'this_month', 'later', 'someday_maybe']

		self.print_html('MissionViewer.html',
						full_mission=full_mission,
						time_frame_sets=time_frame_sets,
						time_frame=time_frame,
						todays_questions_now=todays_questions_now,
						todays_questions_latter=todays_questions_latter,
						reactive_mission=reactive_mission, 
						constants=constants,
						today=today,
						tags=tags)

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return

	def generate_todays_mission(self, time_frame):

		theory = self.theory
		user_key = theory.key
		
		day_start_time = theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		today =(datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).date()
		today_ordinal =(datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).date().toordinal()
	
		current_time = (datetime.today()+timedelta(hours=theory.timezone)).time()

		ksu_set = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False, KSU.in_graveyard == False, KSU.is_active == True)

		if theory.hide_private_ksus:
			ksu_set = ksu_set.filter(KSU.is_private == False)
		
		if time_frame == 'Today':
			ksu_set = ksu_set.order(KSU.best_time).order(KSU.importance).fetch()
		else:
			ksu_set = ksu_set.order(KSU.next_event).order(KSU.importance).order(KSU.best_time).fetch()

		full_mission = {
			'today':{
				'horizon_title':'Today',
				'horizon_set':[],
				'horizon_value':0},

			'timeless_today':{
				'horizon_title':'Timeless Today',
				'horizon_set':[],
				'horizon_value':0},
		 	
		 	'tomorrow':{
		 		'horizon_title':'Tomorrow',
				'horizon_set':[],
				'horizon_value':0},
			
			'this_week':{
				'horizon_title':'This Week',
				'horizon_set':[],
				'horizon_value':0},
			
			'this_month':{
				'horizon_title':'This Month',
				'horizon_set':[],
				'horizon_value':0},
			
			'later':{
				'horizon_title':'Later',
				'horizon_set':[],
				'horizon_value':0},
		 	
		 	'someday_maybe':{
		 		'horizon_title':'Someday ... maybe',
				'horizon_set':[],
				'horizon_value':0},

			'EVPo_someday_maybe':{
		 		'horizon_title':'Joy Generators Someday ... maybe',
				'horizon_set':[],
				'horizon_value':0}}


		def define_horizon(ksu, today_ordinal):
			next_event = ksu.next_event

			if not next_event:
				if ksu.ksu_subtype == 'EVPo':
					return 'EVPo_someday_maybe'
				else:
					return 'someday_maybe'

			next_event = next_event.toordinal()

			if next_event <= today_ordinal:
				if ksu.best_time:
					return 'today'
				else:
					return 'timeless_today'

			if next_event - 1 <= today_ordinal:
				return 'tomorrow'

			if next_event - 7 <= today_ordinal:
				return 'this_week'

			if next_event - 30 <= today_ordinal:
				return 'this_month'

			else:
				return 'later'


		todays_questions_now = []
		todays_questions_latter = []		
		reactive_mission = []

		mission_sets = ['KAS1', 'KAS2', 'EVPo', 'ImPe']
		questions_sets = ['RealitySnapshot', 'BinaryPerception', 'FibonacciPerception', 'Diary']

		for ksu in ksu_set:
			ksu_subtype = ksu.ksu_subtype
	
			next_event = ksu.next_event
			ksu.description_rows = determine_rows(ksu.description)
			ksu.secondary_description_rows = determine_rows(ksu.secondary_description)

			if ksu_subtype in mission_sets:
				time_horizon = define_horizon(ksu, today_ordinal)
				full_mission[time_horizon]['horizon_set'].append(ksu)
				## Apendix - TBD
				if not ksu.kpts_value:
					ksu.kpts_value = 0
				#
				full_mission[time_horizon]['horizon_value'] += ksu.kpts_value

			elif ksu_subtype in questions_sets:
				if today >= next_event:
					if ksu.best_time:					
						if current_time >= ksu.best_time:
							todays_questions_now.append(ksu)
						else:
							todays_questions_latter.append(ksu)
					else:
						todays_questions_latter.append(ksu)

			elif ksu_subtype in ['KAS3','KAS4'] and today >= next_event:
				reactive_mission.append(ksu)
		
		full_mission['today'] = {
			'horizon_title':'Today',
			'horizon_set':full_mission['today']['horizon_set'] + full_mission['timeless_today']['horizon_set'],
			'horizon_value':full_mission['today']['horizon_value'] + full_mission['timeless_today']['horizon_value']}

		return todays_questions_now, todays_questions_latter, reactive_mission, today, full_mission


class EventHandler(Handler):
	
	@super_user_bouncer
	def post(self):
			
		event_details = json.loads(self.request.body)
		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		user_action = event_details['user_action']

		print
		print 'Si llego el AJAX Request. User action: ' + user_action + '. Event details: ' +  str(event_details)
		print


		if user_action == 'SaveNewKSU':			
			ksu = KSU(theory=self.theory.key)
			
			if not 'is_active' in event_details:
				event_details['is_active'] = True

			new_event_details = event_details.copy()
			for a_key in event_details:
				a_val = event_details[a_key]
				if a_val == '':
					del new_event_details[a_key]

			ksu = prepareInputForSaving(self.theory, ksu, new_event_details) #xx
			ksu.put()

			self.response.out.write(json.dumps({
				'mensaje':'KSU creado y guardado desde el viewer!',
				'ksu_id': ksu.key.id(),
				'description': ksu.description,
				# 'next_event': ksu.next_event,
				'kpts_value':ksu.kpts_value
				}))
			return

		if user_action == 'DeleteEvent':
			print
			print 'Si llego el AJAX Request. User action: ' + user_action + '. Event details: ' +  str(event_details)
			print
			
			event = Event.get_by_id(int(event_details['event_id']))
			kpts_type = event.kpts_type
			score = event.score

			active_log = self.active_log
			Streak = active_log.Streak
	
			EffortReserve = active_log.EffortReserve
			Goal = active_log.Goal

			if kpts_type == 'Stupidity':
				active_log.Stupidity -= score
				score = score * (-1)
				
			elif kpts_type == 'SmartEffort':
				active_log.SmartEffort -= score

			else:
				score = 0

			new_SmartEffort = active_log.SmartEffort
			new_Stupidity = active_log.Stupidity


			minimum_daily_effort = self.theory.kpts_goals['minimum_daily_effort']			
			new_EffortReserve = EffortReserve - score
			active_log.EffortReserve = new_EffortReserve

			
			new_PointsToGoal = Goal - new_SmartEffort + new_Stupidity 
			if new_PointsToGoal < 0:
				new_PointsToGoal = 0
			active_log.PointsToGoal = new_PointsToGoal
			
			if not active_log.goal_achieved and new_PointsToGoal == 0:
				active_log.goal_achieved = True				
				active_log.Streak += 1
				active_log.EffortReserve = new_EffortReserve - minimum_daily_effort
			
			elif active_log.goal_achieved and new_PointsToGoal > 0:
				active_log.goal_achieved = False				
				active_log.Streak -= 1
				active_log.EffortReserve = new_EffortReserve + minimum_daily_effort

			active_log.put()
 			
			event.is_deleted = True
			event.put()
			
			ksu = KSU.get_by_id(event.ksu_id.id())
			ksu.in_graveyard = False
			ksu.is_deleted = False
			day_start_time = self.theory.day_start_time
			user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
			today =(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour))
			ksu.next_event = today
			ksu.put()

			self.response.out.write(json.dumps({
				'mensaje':'Evento revertido',
				'PointsToGoal':active_log.PointsToGoal,
				'EffortReserve':active_log.EffortReserve,
				'Streak':active_log.Streak})) 
			return

		print
		print 'Si llego el AJAX Request. User action: ' + user_action + '. Event details: ' +  str(event_details)
		print

		if user_action == 'UpdateKsuAttribute':
			if event_details['content_type'] == 'Event':
				ksu = Event.get_by_id(int(event_details['ksu_id']))	
			else:
				ksu = KSU.get_by_id(int(event_details['ksu_id']))

			attr_key = event_details['attr_key']
			attr_value = event_details['attr_value']			
			updated_value = self.update_single_attribute(ksu, attr_key, attr_value)
			self.response.out.write(json.dumps({'updated_value':updated_value}))
			return

		ksu = KSU.get_by_id(int(event_details['ksu_id']))
		ksu_subtype = ksu.ksu_subtype

		event = Event(
			theory=self.theory.key,
			ksu_id =  ksu.key,
			event_type = user_action,
			user_date=(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour)).toordinal(),
			comments = event_details['event_comments'].encode('utf-8'),
			secondary_comments = event_details['event_secondary_comments'].encode('utf-8'),
			ksu_description = ksu.description,
			ksu_subtype = ksu.ksu_subtype, 
			ksu_tags = ksu.tags)
			

		if user_action == 'RecordValue':
			event.kpts_type = 'IndicatorValue'
			event.score = float(event_details['kpts_value'])
			update_next_event(self, user_action, {}, ksu)
			event.put()	

		if user_action in ['MissionDone', 'ViewerDone']:

			if ksu_subtype in ['KAS1', 'KAS2', 'KAS3', 'EVPo', 'ImPe']:
				event.kpts_type = 'SmartEffort'
				event.score = float(event_details['kpts_value'])
				
				if ksu_subtype == 'KAS2':
					ksu.is_deleted = True

				update_next_event(self, user_action, {}, ksu) #xx
			
				if ksu_subtype in ['ImPe']:
					event.ksu_description = ksu.secondary_description

			if ksu_subtype == 'KAS4':
				event.kpts_type = 'Stupidity'
				event.score = float(event_details['kpts_value'])				

			if ksu_subtype == 'BigO':
				event.kpts_type = 'Achievement'				
				ksu.in_graveyard = True

			if ksu_subtype == 'Wish':				
				event.kpts_type = 'Excitement'
				ksu.in_graveyard = True
				
			self.update_active_log(event)
			event.put()

		if user_action in ['MissionPush', 'MissionSkip', 'SendToMission']:
			update_next_event(self, user_action, {}, ksu)
			

		if user_action == 'ViewerOnOff':
			if ksu.is_active:
				ksu.is_active = False
			else:
				ksu.is_active = True
			


		if user_action in ['MissionDelete', 'ViewerDelete']:
			ksu.in_graveyard = True
			if ksu_subtype in ['Gene','KAS2']:
				ksu.is_deleted = True
			

		if user_action == 'GraveyardReanimate':
			ksu.in_graveyard = False
			

		if user_action == 'GraveyardDelete':
			ksu.is_deleted = True
					
		ksu.put()
		
		active_log = self.active_log
		PointsToGoal = active_log.PointsToGoal
		EffortReserve = active_log.EffortReserve
		Streak = active_log.Streak


		self.response.out.write(json.dumps({'mensaje':'Evento creado y guardado', 
											
											'event_comments':event.comments,
											'EventScore':event.score, 											
											'kpts_type':event.kpts_type, 
											
											'ksu_subtype':ksu_subtype, 
											'kpts_value':ksu.kpts_value,
											'pretty_next_event':ksu.pretty_next_event,
											'is_active':ksu.is_active,
											
											'PointsToGoal':PointsToGoal,
											'EffortReserve':EffortReserve,
											'Streak':Streak}))
		return


	def update_active_log(self, event):
		active_log = self.active_log
		minimum_daily_effort = self.theory.kpts_goals['minimum_daily_effort']

		if event.kpts_type == 'SmartEffort':
			active_log.SmartEffort += event.score
			active_log.PointsToGoal -= event.score
			active_log.EffortReserve += event.score

		if event.kpts_type == 'Stupidity':
			active_log.Stupidity += event.score
			active_log.PointsToGoal += event.score
			active_log.EffortReserve -= event.score

		if not active_log.goal_achieved and active_log.PointsToGoal <= 0:
			active_log.goal_achieved = True
			active_log.Streak += 1
			active_log.EffortReserve -= minimum_daily_effort 

		if active_log.PointsToGoal < 0:
			active_log.PointsToGoal = 0

		active_log.put()
		

	def update_single_attribute(self, ksu, attr_key, attr_value):
		updated_value = None
		
		if attr_key in ['description', 'secondary_description', 'comments', 'repeats', 'secondary_comments']:
			setattr(ksu, attr_key, attr_value.encode('utf-8'))		
			updated_value = attr_value.encode('utf-8')

		elif attr_key == 'best_time':
			if attr_value == '':
				ksu.best_time = None
				ksu.pretty_best_time = None
				ksu.put()
				return None
			attr_val = attr_value[0:5]
			ksu.best_time = datetime.strptime(attr_value, '%H:%M').time()
			ksu.pretty_best_time = attr_value
			updated_value = ksu.pretty_best_time
		
		elif attr_key == 'next_event':
			if attr_value == '':
				ksu.next_event = None
				ksu.pretty_next_event = None
				ksu.put()
				return None
			ksu.next_event = datetime.strptime(attr_value, '%Y-%m-%d')
			ksu.pretty_next_event = datetime.strptime(attr_value, '%Y-%m-%d').strftime('%a, %b %d, %Y')
			updated_value = ksu.next_event.strftime('%a, %b %d, %Y')

		elif attr_key == 'birthday':
			ksu.birthday = datetime.strptime(attr_value, '%Y-%m-%d')
			updated_value = ksu.birthday.strftime('%a, %b %d, %Y')

		elif attr_key == 'kpts_value':
			ksu.kpts_value = float(attr_value)
			updated_value = ksu.kpts_value 

		elif attr_key == 'tags':
			theory = self.theory
			attr_value, tags = prepare_tags_for_saving(attr_value)
			ksu.tags = attr_value.encode('utf-8')
			update_user_tags(theory, tags)
			theory.categories['tags'] = update_user_tags(theory, tags)
			theory.put()

		elif attr_key in ['importance', 'frequency', 'money_cost']:
			setattr(ksu, attr_key, int(attr_value))	
			updated_value = int(attr_value)

		elif attr_key in ['is_critical', 'is_private', 'is_active']:
			if attr_value == 'on':
				attr_value = True
			setattr(ksu, attr_key, attr_value)

		elif attr_key in ['repeats_on_Mon', 'repeats_on_Tue', 'repeats_on_Wed', 'repeats_on_Thu', 'repeats_on_Fri', 'repeats_on_Sat', 'repeats_on_Sun']:
			ksu.repeats_on[attr_key] = attr_value 

		ksu.put()	
		return updated_value


	def create_new_ksu_from_viewer(self):
		return


class HistoryViewer(Handler):

	@super_user_bouncer
	def get(self):
		history_title = 'History'
		ksu_id = self.request.get('ksu_id')
		
		diary_view = False

		if ksu_id:
			ksu = KSU.get_by_id(int(ksu_id))
			if ksu.ksu_subtype == 'Diary':
				history_title = ksu.description
				diary_view = True
			else:
				history_title = 'KSU history'

		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		today =(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour)).date().toordinal()


		history_start = self.request.get('history_start')
		if history_start:
			history_start = int(history_start)
		elif ksu_id:
			history_start = (self.theory.created).toordinal()
		else:
			history_start = today

		history_end = self.request.get('history_end')
		if history_end:
			history_end = int(history_end)
		else:
			history_end = today

		history, history_value = self.retrieve_history(ksu_id, history_start, history_end)
		history_start = datetime.fromordinal(history_start)
		history_end = datetime.fromordinal(history_end)

		self.print_html('HistoryViewer.html', diary_view=diary_view, history_title=history_title, history=history, history_start=history_start, history_end=history_end, history_value=history_value, constants=constants)


	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):

		redirect_to = '/HistoryViewer'

		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0
		today =(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour)).date().toordinal()

		print
		print 'These are the post details:'
		print post_details
		print
		
		if 'post_history_start' in post_details:
			history_start = (datetime.strptime(post_details['post_history_start'], '%Y-%m-%d')).date().toordinal()
			redirect_to += '?history_start='+str(history_start)

		
		if 'post_history_end' in post_details:
			history_end = (datetime.strptime(post_details['post_history_end'], '%Y-%m-%d')).date().toordinal()
			redirect_to += '&history_end='+str(history_end)

		if 'ksu_id' in post_details:
			redirect_to += '&ksu_id='+ post_details['ksu_id']			
		
		self.redirect(redirect_to)
		return

	def retrieve_history(self, ksu_id, history_start, history_end): #xx
		user_key = self.theory.key
		
		if ksu_id:
			ksu = KSU.get_by_id(int(ksu_id))
			ksu_key = ksu.key
			if ksu.ksu_subtype == 'Diary':
				event_set =	Event.query(Event.ksu_id == ksu_key).filter(Event.is_deleted == False).order(Event.importance).order(-Event.user_date,-Event.created)
				if self.theory.hide_private_ksus:
					event_set = event_set.filter(Event.is_private == False)
				event_set = event_set.fetch()
				
			else:
				event_set = Event.query(Event.ksu_id == ksu_key).filter(Event.is_deleted == False, Event.user_date >= history_start, Event.user_date <= history_end).order(-Event.user_date,-Event.created).fetch()
		else:
			event_set = Event.query(Event.theory == user_key).filter(Event.is_deleted == False, Event.user_date >= history_start, Event.user_date <= history_end).order(-Event.user_date,-Event.created).fetch()
		
		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0

		history = []
		history_value = 0

		for event in event_set: #xx
			ksu = KSU.get_by_id(event.ksu_id.id())
			## Apendix - TBD once my theory is updated
			ksu_subtype = ksu.ksu_subtype
			if ksu_subtype in ['ImPe']:
				event.ksu_description = ksu.secondary_description
			else:
				event.ksu_description = ksu.description
			event.ksu_subtype = ksu_subtype
			event.ksu_tags = ksu.tags
			if not event.importance:
				event.importance = 3
			event.put()
			##
			event.pretty_date = (event.user_date_date+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour)).date().strftime('%a, %b %d, %Y')
			event.comments_rows = determine_rows(event.comments)

			history.append(event)
			if event.ksu_subtype in ['KAS1', 'KAS2', 'KAS3', 'EVPo', 'ImPe']:
				history_value += event.score
			elif event.ksu_subtype == 'KAS4':
				history_value -= event.score

		return history, history_value


#--- Development handlers ----------
class PopulateRandomTheory(Handler):
	
	def get(self):
		self.populateRandomTheory()
		self.redirect('/MissionViewer?time_frame=Today')

	def populateRandomTheory(self):

		post_details = {'user_action':'Random_SignUp'}
		user_action = 'Random_SignUp'

		if user_action == 'Random_SignUp':
			post_details.update(randomUser.createRandomUser()) ## Creates a random user for testing purposes
		
		if user_action == 'SignUp' or user_action == 'Random_SignUp':
			input_error = user_input_error(post_details)
			theory = Theory.get_by_email(post_details['email'])	
			
			if input_error:
				self.print_html('SignUpLogIn.html', post_details=post_details, input_error=input_error)
			
			elif theory:
				self.print_html('SignUpLogIn.html', post_details=post_details, input_error = 'That email is already register to another user!')

			else:
				password_hash = make_password_hash(post_details['email'], post_details['password'])
				
				kpts_goals_parameters = {
						'typical_week_effort_distribution':[1, 1, 1, 1, 1, 0.5, 0],
						'yearly_vacations_day': 12,
						'yearly_shit_happens_days': 6,
						'minimum_daily_effort':20}

				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					day_start_time=datetime.strptime('06:00', '%H:%M').time(),
					timezone=-4,
					kpts_goals_parameters=kpts_goals_parameters,
					kpts_goals=calculate_user_kpts_goals(kpts_goals_parameters),
					categories={'tags':[]},
					last_DailyLog = datetime.today().toordinal())

				theory.put()

				#creates the first DailyLog entry
				day_start_time = theory.day_start_time
				user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
				active_date = (datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).toordinal() 
				active_date_date = datetime.fromordinal(active_date)
				active_weekday = (datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour)).weekday()
				goal = int(theory.kpts_goals['kpts_weekly_goals'][active_weekday])
				
				
				active_log = DailyLog(
					theory = theory.key,
					
					user_date_date = active_date_date,
					user_date = active_date,
					streak_start_date = active_date,
					
					Goal = goal,
					PointsToGoal=goal)
				active_log.put()

				theory.last_DailyLog = active_date
				theory.put()

				#Loads OS Ksus
				for post_details in os_ksus:
					ksu = KSU(theory=theory.key)
					ksu = prepareInputForSaving(theory, ksu, post_details)
					ksu.put()

				self.login(theory)
				# self.redirect('/MissionViewer?time_frame=Today')


		theory_key = theory.key
		username = theory.first_name + ' ' + theory.last_name

		day_start_time = theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 		
		today =(datetime.today()+timedelta(hours=theory.timezone)-timedelta(hours=user_start_hour))

		theory_parameters = [
			[0	,{'ksu_type':'Gene', 'ksu_subtype':'Gene'}],
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS1', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':2, 'frequency':1, 'repeats':'R001'}],
			[0, {'ksu_type':'OTOA', 'ksu_subtype':'KAS2', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':3}],
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS3', 'kpts_value':0.25}],
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS4', 'kpts_value':5}],
			[0, {'ksu_type':'BigO', 'ksu_subtype':'BigO'}],
			[0, {'ksu_type':'Wish', 'ksu_subtype':'Wish'}],
			[0, {'ksu_type':'EVPo', 'ksu_subtype':'EVPo', 'next_event':today, 'kpts_value':1, 'frequency':7}],
			[0, {'ksu_type':'ImPe', 'ksu_subtype':'ImPe', 'next_event':today, 'kpts_value':0.25, 'frequency':30}],
			[0, {'ksu_type':'Idea', 'ksu_subtype':'Idea'}],
			[0, {'ksu_type':'RTBG', 'ksu_subtype':'RTBG'}],
			[0, {'ksu_type':'Diary', 'ksu_subtype':'Diary', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'RealitySnapshot', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'BinaryPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'FibonacciPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}]
		]

		for e in theory_parameters:
			set_size = e[0]
			set_details = e[1]

			ksu_subtype = constants['d_KsuSubtypes'][set_details['ksu_subtype']]

			for i in range(1, set_size + 1):

				description =  str(ksu_subtype + ' no. ' + str(i) + ' of ' + username).encode('utf-8')
				secondary_description = str('Secondary description of ' + ksu_subtype + ' no. ' + str(i)).encode('utf-8')
				new_ksu = KSU(
					theory=theory_key,
					description=description,
					secondary_description=secondary_description)

				for a_key in set_details:
					a_val = set_details[a_key]
					setattr(new_ksu, a_key, a_val)
			
				
				next_event = new_ksu.next_event
				ksu_subtype = new_ksu.ksu_subtype

				if ksu_subtype in ['KAS1','KAS3','KAS4','ImPe'] and not next_event:
					new_ksu.next_event = today

				new_ksu.put()		
		return


#--- Essential Helper Functions ----------
def get_post_details(self):
	post_details = {}
	arguments = self.request.arguments()
	for argument in arguments:
		post_details[str(argument)] = self.request.get(str(argument))
	return adjust_post_details(post_details)

def adjust_post_details(post_details): 
	details = {}
	for (attribute, value) in post_details.items():
		if value and value!='' and value!='None':
			details[attribute] = value
	return details

def determine_return_to(self):

	return_to = self.request.get('return_to')
	if not return_to:
		return_to = self.request.path
	
	set_name = self.request.get('set_name')
	if set_name:
		return_to += '?set_name=' + set_name

	time_frame = self.request.get('time_frame')
	if time_frame:
		return_to += '?time_frame=' + time_frame


	return return_to

def calculate_user_kpts_goals(kpts_goals_parameters):

	minimum_daily_effort = kpts_goals_parameters['minimum_daily_effort']
	yearly_vacations_day = kpts_goals_parameters['yearly_vacations_day']
	yearly_shit_happens_days = kpts_goals_parameters['yearly_shit_happens_days']
	typical_week_effort_distribution = kpts_goals_parameters['typical_week_effort_distribution']
	typical_week_active_days = sum(typical_week_effort_distribution)

	yearly_effort_goal = minimum_daily_effort * 365.25
	active_days = 365.25 - (yearly_vacations_day + yearly_shit_happens_days) - ((7 - typical_week_active_days) * (365.25/7.0))
	
	typical_day_minimum_effort = yearly_effort_goal/active_days

	kpts_weekly_goals = []
	for e in typical_week_effort_distribution:
		kpts_weekly_goals.append(math.ceil(e * typical_day_minimum_effort))

	user_kpts_goals = {
		'minimum_daily_effort':minimum_daily_effort,
		'typical_day_minimum_effort': math.ceil(typical_day_minimum_effort),
		'kpts_weekly_goals': kpts_weekly_goals,
		'active_days': math.ceil(active_days)
	}

	return user_kpts_goals

def update_next_event(self, user_action, post_details, ksu):

	def days_to_next_event(ksu):

		def find_next_weekly_repetition(d_repeats_on):

			def d_to_l_repeats_on(d_repeats_on):
				result = []
				l_repeats_on_keys = ['repeats_on_Mon', 'repeats_on_Tue', 'repeats_on_Wed', 'repeats_on_Thu', 'repeats_on_Fri', 'repeats_on_Sat', 'repeats_on_Sun']
				for day in l_repeats_on_keys:
					result.append(d_repeats_on[day])
				return result

			l_repeats_on = d_to_l_repeats_on(d_repeats_on)

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

			day_start_time = self.theory.day_start_time
			user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
			today =(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour))

			active_position = today.weekday()

			repeats_on_list = reorginize_list(l_repeats_on, active_position)

			i = 1
			for weekday in repeats_on_list:
				if weekday:
					return i
				else:
					i += 1
			return 0

		d_repeats_values = {'R000':'Never', 'R001':1, 'R007':7, 'R030':30, 'R365':365}
		
		repeats = ksu.repeats
		repeats_on = ksu.repeats_on
		frequency = ksu.frequency

		result = 0

		if repeats in ['R001', 'R030', 'R365']:		
			result = d_repeats_values[repeats] * frequency

		if repeats == 'R007':
			result = find_next_weekly_repetition(repeats_on)

		return result
	

	day_start_time = self.theory.day_start_time
	user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
	today =(datetime.today()+timedelta(hours=self.theory.timezone)-timedelta(hours=user_start_hour))
	tomorrow = today + timedelta(days=1)
	ksu_subtype = ksu.ksu_subtype	
	
	if ksu_subtype == 'KAS1':
		next_event = ksu.next_event
		days_to_next_event = days_to_next_event(ksu)

		if not next_event:
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')
			
		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone']:
			ksu.next_event = today + timedelta(days=days_to_next_event)
			ksu.pretty_next_event = (today + timedelta(days=days_to_next_event)).strftime('%a, %b %d, %Y')

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

		if user_action == 'SendToMission':
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')
			print ksu.pretty_next_event

	elif ksu_subtype in ['KAS2', 'EVPo']:

		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone']:
			ksu.next_event = None
			ksu.pretty_next_event = None

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

		if user_action == 'SendToMission':
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')


	elif ksu_subtype in ['KAS3', 'KAS4']:
		
		next_event = ksu.next_event

		if not next_event:
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')

		if user_action in ['MissionDone']:
			ksu.next_event = today
			ksu.pretty_next_event = today.strftime('%a, %b %d, %Y')

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')


	elif ksu_subtype in ['ImPe', 'RealitySnapshot', 'FibonacciPerception', 'BinaryPerception', 'Diary']:
		
		next_event = ksu.next_event

		if not next_event:
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')

		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone', 'RecordValue']:
			ksu.next_event = today + timedelta(days=ksu.frequency)
			ksu.pretty_next_event = (today + timedelta(days=ksu.frequency)).strftime('%a, %b %d, %Y')

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')



	return		

def prepareInputForSaving(theory, ksu, post_details):

	def determine_ksu_subtype(ksu, post_details):

		ksu_type = ksu.ksu_type

		if 'ksu_subtype' in post_details:
			ksu_subtype = post_details['ksu_subtype']
		else:
			ksu_subtype = ksu_type

		if ksu_type == 'OTOA':
			ksu_subtype = 'KAS2'

		return ksu_subtype


	l_checkbox_attribute = [ 'is_active', 
							 'is_critical', 
							 'is_private']

	d_repeats_on = {
		'repeats_on_Mon': False,
		'repeats_on_Tue': False, 
		'repeats_on_Wed': False, 
		'repeats_on_Thu': False,
		'repeats_on_Fri': False,
		'repeats_on_Sat': False,
		'repeats_on_Sun': False}

	for attribute in l_checkbox_attribute:
		setattr(ksu, attribute, False)

	d_attributeType = constants['d_attributeType']

	for a_key in post_details:

		a_val = post_details[a_key]
		a_type = None
		
		if a_key in d_attributeType:
			a_type = d_attributeType[a_key]
		
		if a_type == 'string':
			setattr(ksu, a_key, a_val.encode('utf-8'))

		if a_type == 'integer':
			setattr(ksu, a_key, int(a_val))

		if a_type == 'float':
			setattr(ksu, a_key, float(a_val))

		if a_type == 'date':
			setattr(ksu, a_key, datetime.strptime(a_val, '%Y-%m-%d'))
			if a_key == 'next_event':
				setattr(ksu, 'pretty_'+a_key, datetime.strptime(a_val, '%Y-%m-%d').strftime('%a, %b %d, %Y'))

		if a_type == 'time':
			a_val = a_val[0:5]
			setattr(ksu, a_key, datetime.strptime(a_val, '%H:%M').time())
			setattr(ksu, 'pretty_'+a_key, a_val)

		if a_type == 'checkbox':
			if a_val == 'on':
				a_val = True
			setattr(ksu, a_key, a_val)

		if a_type == 'checkbox_repeats_on':
			if a_val == 'on':
				a_val = True
			d_repeats_on[a_key] = a_val

		if a_type =='user_tags':
			a_val, tags = prepare_tags_for_saving(a_val)
			setattr(ksu, a_key, a_val.encode('utf-8'))
			update_user_tags(theory, tags)
			theory.categories['tags'] = update_user_tags(theory, tags)
			theory.put()

	setattr(ksu, 'repeats_on', d_repeats_on)
	
	ksu.ksu_subtype = determine_ksu_subtype(ksu, post_details)

	if ksu.ksu_subtype == 'ImPe' and not ksu.secondary_description:
		ksu.secondary_description = 'Contact ' + ksu.description

	if ksu.ksu_subtype in ['KAS1','KAS3','KAS4','ImPe', 'RealitySnapshot', 'Diary', 'FibonacciPerception', 'BinaryPerception'] and not ksu.next_event:
		ksu.next_event = datetime.today() - timedelta(days=1)
	print ksu.ksu_type
	print ksu.next_event

	if ksu.ksu_subtype in ['KAS1','KAS3','KAS4','ImPe', 'RealitySnapshot', 'Diary', 'FibonacciPerception', 'BinaryPerception'] and not ksu.frequency:
		ksu.frequency = 1

	return ksu

def remplaza_acentos(palabra):
	# -*- coding: utf-8 -*-
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
	palabra = palabra.encode('utf-8')
	palabra = palabra.decode('utf-8')
	for letra in letras_a_remplazar:
		palabra = palabra.replace(letra[0].decode('utf-8'),letra[1])

	return palabra

def prepare_tags_for_saving(tags_string):

	tags_string = remplaza_acentos(tags_string)
	valid_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','_',',','1','2','3','4','5','6','7','8','9','0']
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

def update_user_tags(theory, tags):

	current_tags = theory.categories['tags']
	for tag in tags:
		if tag not in current_tags:
			current_tags.append(tag)
	return sorted(current_tags)
	
def determine_rows(ksu_description):
	if not ksu_description:
		return 0
	return int(math.ceil((len(ksu_description)/64.0)))


#--- Validation and security functions ----------
secret = 'elzecreto'

def make_secure_val(val):
    return '%s|%s' % (val, hashlib.sha256(secret + val).hexdigest())

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val

def make_salt(lenght = 5):
    return ''.join(random.choice(string.letters) for x in range(lenght))

def make_password_hash(email, password, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(email + password + salt).hexdigest()
	return '%s|%s' % (h, salt)

def validate_password(email, password, h):
	salt = h.split('|')[1]
	return h == make_password_hash(email, password, salt)

def user_input_error(post_details):
	for (attribute, value) in post_details.items():
		user_error = input_error(attribute, value)
		if user_error:
			return user_error

	if 'confirm_email' in post_details:
		if post_details['email'] != post_details['confirm_email']:
			return "Emails don't match"

	return None

def input_error(target_attribute, user_input):
	
	validation_attributes = ['first_name',
							 'last_name', 
							 'password',
							 'email']


	if target_attribute not in validation_attributes:
		return None
	
	error_key = target_attribute + '_error' 
		
	if d_RE[target_attribute].match(user_input):
		return None

	else:
		return d_RE[error_key]

d_RE = {'first_name': re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
		'first_name_error': 'invalid first name syntax',
		
		'last_name': re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
		'last_name_error': 'invalid last name syntax',

		'password': re.compile(r"^.{3,20}$"),
		'password_error': 'invalid password syntax',
		
		'email': re.compile(r'^[\S]+@[\S]+\.[\S]+$'),
		'email_error': 'invalid email syntax'}



#--- Request index
app = webapp2.WSGIApplication([
							    ('/', SetViewer),
							    ('/SignUpLogIn', SignUpLogIn),
							    ('/LogOut', LogOut),
							    ('/Settings', Settings),
							    
							    ('/KsuEditor', KsuEditor),
							    ('/MissionViewer', MissionViewer),
							    ('/SetViewer', SetViewer),
						
							    ('/EventHandler',EventHandler),
							    ('/HistoryViewer', HistoryViewer),

							    ('/PopulateRandomTheory',PopulateRandomTheory)
								], debug=True)

