#KASware V2.0.0 | Copyright 2016 Kasware Inc.
import webapp2, jinja2, os, re, random, string, hashlib, json, logging, math 

from datetime import datetime, timedelta, time
from google.appengine.ext import ndb
from python_files import datastore, randomUser, constants

constants = constants.constants
Theory = datastore.Theory
KSU = datastore.KSU
Event = datastore.Event
DailyLog = datastore.DailyLog


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

	def print_html(self, template, **kw):
		self.write(self.render_html(template, **kw))

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
		
		day_start_time = theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 

		active_date = (datetime.today()-timedelta(hours=user_start_hour)).toordinal()  	
		user_key = theory.key

		active_log = DailyLog.query(DailyLog.theory == user_key ).filter(DailyLog.user_date_ordinal == active_date).fetch()
		
		if active_log:
			active_log = active_log[0]

		if not active_log:

			active_weekday = (datetime.today()-timedelta(hours=user_start_hour)).weekday()
			goal = int(theory.kpts_goals['typical_weekly_goals'][active_weekday])

			active_log = DailyLog(
				theory = theory.key,
				user_date_ordinal = active_date,
				Goal = goal)
			active_log.put()

		return active_log


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

				categories = {
					'Global':[
						'Unassigned',
						'0. End Value'
						'1. Inner Peace & Consciousness',
						'2. Fun & Exciting Situations', 	
						'3. Meaning & Direction',
						'4. Health & Vitality', 
						'5. Love & Friendship', 
						'6. Knowledge & Skills', 
						'7. Outer Order & Peace', 
						'8. Stuff',
						'9. Money & Power'],
					'Gene': ['Unassigned'],
					'KeyA': ['Unassigned'],
					'BigO': ['Unassigned'],
					'Wish': [	
						'Unassigned',	
						'01. Being',
						'02. Having',
						'03. Doing',
						'04. Geting done',
						'05. TV Show',
						'06. Movie',
						'07. Tesis',
						'08. Novel',
						'09. Video Game',
						'10. Board Game',
						'11. City'],	
					'Prin': ['Unassigned'],
					'EVPo': ['Unassigned'],
					'ImPe': ['Unassigned'],
					'RTBG': ['Unassigned'],
					'Idea': ['Unassigned'],
					'NoAR': ['Unassigned'],
					'MoRe': ['Unassigned'],
					'ImIn': ['Unassigned']}

				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					day_start_time=datetime.strptime('06:00', '%H:%M').time(),
					kpts_goals_parameters=kpts_goals_parameters,
					kpts_goals=calculate_user_kpts_goals(kpts_goals_parameters),
					categories=categories)

				theory.put()
				self.login(theory)
				self.redirect('/')

		if user_action == 'LogIn':			
			email = self.request.get('email')
			password = self.request.get('password')
			theory = Theory.valid_login(email, password)
			if theory:
				self.login(theory)
				self.redirect('/')
			else:
				self.write('incorrect username or password')


class LogOut(Handler):
	def get(self):
		self.logout()
		self.redirect('/')


class Settings(Handler):

	@super_user_bouncer
	def get(self):
		self.print_html('Settings.html', ksu={}, constants=constants)


class KsuEditor(Handler):
	
	@super_user_bouncer
	def get(self):
		ksu_id = self.request.get('ksu_id')
		if ksu_id == 'NewKSU':
			ksu = constants['default_ksu']
		else: 
			ksu = KSU.get_by_id(int(ksu_id))
		categories = self.theory.categories
		self.print_html('KsuEditor.html', ksu=ksu, constants=constants, categories=categories)

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
			print
			print 'REQUEST TO SAVE KSU:'
			print 'POST DETAILS:'
			print post_details
			print
			print

			ksu = self.prepareInputForSaving(ksu, post_details)
			update_next_event(self, user_action, post_details, ksu)
			ksu.put()
		
		self.redirect(return_to)

		# self.write(post_details)
		return



	def prepareInputForSaving(self, ksu, post_details):

		l_checkbox_attribute = [ 'is_active', 
								 'is_critical', 
								 'is_private',
								 'is_BigO',
								 'is_dream', 
								 'is_principle', 
								 'was_awesome',
								 'reverse_target']

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
				if a_key in ['target_date', 'next_event']:
					setattr(ksu, 'pretty_'+a_key, datetime.strptime(a_val, '%Y-%m-%d').strftime('%a, %b %d, %Y'))


			if a_type == 'time':
				a_val = a_val[0:5]
				setattr(ksu, a_key, datetime.strptime(a_val, '%H:%M').time())

			if a_type == 'checkbox':
				setattr(ksu, a_key, True)

			if a_type == 'checkbox_repeats_on':
				d_repeats_on[a_key] = True

		setattr(ksu, 'repeats_on', d_repeats_on)
		
		ksu.ksu_subtype = self.determine_ksu_subtype(ksu, post_details)

		return ksu

	def determine_ksu_subtype(self, ksu, post_details):

		ksu_type = ksu.ksu_type

		if 'ksu_subtype' in post_details:
			ksu_subtype = post_details['ksu_subtype']
		else:
			ksu_subtype = ksu_type

		if ksu_subtype == 'KAS1or2':
			if ksu.repeats == 'R000':
				ksu_subtype = 'KAS2'
			else:
				ksu_subtype = 'KAS1'

		elif ksu_type == 'BigO':
			if ksu.is_BigO:
				ksu_subtype = 'BigO'
			else:
				ksu_subtype = 'MinO'

		elif ksu_type == 'Wish':
			if ksu.is_dream:
				ksu_subtype = 'Dream'
			else:
				ksu_subtype = 'Wish'

		elif ksu_type == 'Idea':
			if ksu.is_principle:
				ksu_subtype = 'Principle'


		return ksu_subtype


class Home(Handler):
	
	@super_user_bouncer
	def get(self):
		theory = self.theory
		message = 'Welcome to KASware ' + theory.first_name + ' ' + theory.last_name
		self.write(message)


class TodaysMission(Handler):

	@super_user_bouncer
	def get(self):
		user_key = self.theory.key
		ksu_set, mission_value = self.generate_todays_mission()
		self.print_html('TodaysMission.html', ksu_set=ksu_set, mission_value=mission_value,constants=constants)

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return

	#xx
	def generate_todays_mission(self):
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False).order(KSU.created).fetch()

		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
		today =(datetime.today()-timedelta(hours=user_start_hour)).date()
		mission = []
		mission_value = 0
		mission_sets = ['KAS1', 'KAS2', 'EVPo', 'ImPe']
		for ksu in ksu_set:
			ksu_subtype = ksu.ksu_subtype
			if ksu_subtype in mission_sets:
				next_event = ksu.next_event

				if ksu.is_active and next_event and today >= next_event:
					mission.append(ksu)
					mission_value += ksu.kpts_value

		pinned_sets = ['KAS3', 'KAS4']
		return mission, mission_value

			
class SetViewer(Handler):

	@super_user_bouncer
	def get(self):
		set_name = self.request.get('set_name')
		user_key = self.theory.key
		if not set_name:
			ksu_set = KSU.query(KSU.theory == user_key ).order(KSU.created).fetch()	
		else:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.ksu_type == set_name).order(KSU.created).fetch()
		
		self.print_html('SetViewer.html', ksu_set=ksu_set, constants=constants, set_name=set_name)

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return


class EventHandler(Handler):
	
	@super_user_bouncer
	def post(self):

		event_details = json.loads(self.request.body)
		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 

		user_action = event_details['user_action']
		ksu = KSU.get_by_id(int(event_details['ksu_id']))
		ksu_subtype = ksu.ksu_subtype

		print
		print
		print 'Si llego el AJAX Request. User action: ' + user_action + '. Event details: ' +  str(event_details)
		print

		event = Event(
			theory=self.theory.key,
			ksu_id =  ksu.key,
			event_type = user_action,
			user_date_ordinal=(datetime.today()-timedelta(hours=user_start_hour)).toordinal())


		if user_action in ['MissionDone', 'ViewerDone']:

			if ksu_subtype in ['KAS1', 'KAS2', 'KAS3', 'EVPo', 'ImPe']:
				event.kpts_type = 'SmartEffort'
				event.score = float(event_details['kpts_value'])
				
				update_next_event(self, user_action, {}, ksu)
				ksu.put()

			if ksu_subtype == 'KAS4':
				event.kpts_type = 'Stupidity'
				event.score = float(event_details['kpts_value'])				


		self.update_active_log(event)
		event.put()		

		self.response.out.write(json.dumps({'mensaje':'Evento creado y guardado', 'EventScore':event.score, 'kpts_type':event.kpts_type, 'ksu_subtype':ksu_subtype}))
		return

	def update_active_log(self, event):
		active_log = self.active_log
		
		if event.kpts_type == 'SmartEffort':
			active_log.SmartEffort += event.score

		if event.kpts_type == 'Stupidity':
			active_log.Stupidity += event.score

		active_log.put() 


#--- Development handlers ----------
class PopulateRandomTheory(Handler):
	
	def get(self):
		self.populateRandomTheory()
		self.redirect('/')

	def populateRandomTheory(self):

		theory = self.theory
		theory_key = theory.key
		username = theory.first_name + ' ' + theory.last_name

		day_start_time = self.theory.day_start_time
		user_start_hour = day_start_time.hour + day_start_time.minute/60.0 		
		today =(datetime.today()-timedelta(hours=user_start_hour))

		theory_parameters = [
			[10,{'ksu_type':'Gene', 'ksu_subtype':'Gene'}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS1', 'next_event':today, 'kpts_value':2}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS2', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':3}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS3', 'kpts_value':0.25}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS4', 'kpts_value':5}],
			[1, {'ksu_type':'BigO', 'ksu_subtype':'BigO'}],
			[2, {'ksu_type':'BigO', 'ksu_subtype':'MinO'}],
			[3, {'ksu_type':'Wish', 'ksu_subtype':'Wish'}],
			[3, {'ksu_type':'Wish', 'ksu_subtype':'Dream'}],
			[3, {'ksu_type':'EVPo', 'ksu_subtype':'EVPo', 'next_event':today, 'kpts_value':1, 'frequency':7}],
			[3, {'ksu_type':'ImPe', 'ksu_subtype':'ImPe', 'next_event':today, 'kpts_value':0.25, 'frequency':30}],
			[3, {'ksu_type':'Idea', 'ksu_subtype':'Idea'}],
			[5, {'ksu_type':'Idea', 'ksu_subtype':'Principle'}],
			[3, {'ksu_type':'RTBG', 'ksu_subtype':'RTBG'}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'RealitySnapshot'}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'BinaryPerception'}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'FibonacciPerception'}]
		]

		for e in theory_parameters:
			set_size = e[0]
			set_details = e[1]

			ksu_subtype = constants['d_KsuSubtypes'][set_details['ksu_subtype']]

			for i in range(1, set_size + 1):

				description =  ksu_subtype + ' no. ' + str(i) + ' of ' + username
				new_ksu = KSU(
					theory=theory_key,
					description=description)

				for a_key in set_details:
					a_val = set_details[a_key]
					setattr(new_ksu, a_key, a_val)
			
				new_ksu.put()		
		return


class DataStoreViewer(Handler):

	def descriptionsOnly(self):
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key).order(KSU.created).fetch()
		result = []
		for ksu in ksu_set:
			result.append(ksu.description)
		return result	

	def get(self):
		self.write('User: ')
		self.write(self.theory.first_name)
		self.write('<br>')
		self.write('<br>')
		for ksu in self.descriptionsOnly():
			self.write(ksu)
			self.write('<br>') 


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

	typical_weekly_goals = []
	for e in typical_week_effort_distribution:
		typical_weekly_goals.append(math.ceil(e * typical_day_minimum_effort))

	user_kpts_goals = {
		'typical_day_minimum_effort': math.ceil(typical_day_minimum_effort),
		'typical_weekly_goals': typical_weekly_goals,
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

			active_position = datetime.today().weekday()
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
	# today = datetime.today() + timedelta(days=20)

	day_start_time = self.theory.day_start_time
	user_start_hour = day_start_time.hour + day_start_time.minute/60.0 
	today =(datetime.today()-timedelta(hours=user_start_hour))
	tomorrow = today + timedelta(days=1)
	ksu_subtype = ksu.ksu_subtype	
	days_to_next_event = days_to_next_event(ksu)

	if ksu_subtype == 'KAS1':
		next_event = ksu.next_event

		if not next_event:
			ksu.next_event = today
			
		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone']:
			ksu.next_event = today + timedelta(days=days_to_next_event)

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow

		ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

	if ksu_subtype == 'KAS2':
		next_event = ksu.next_event

		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone']:
			ksu.next_event = None
			ksu.pretty_next_event = None

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

	if ksu_subtype in ['EVPo', 'ImPe']:
		next_event = ksu.next_event

		if not next_event:
			ksu.next_event = today

		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone']:
			ksu.next_event = today + timedelta(days=ksu.frequency)			

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow

		ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')


	return		

def kill_ksu(ksu): #xx
	ksu.is_active = False
	ksu.is_deleted = True
	ksu.in_graveyard = True
	return ksu



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
							    ('/', TodaysMission),
							    
							    ('/SignUpLogIn', SignUpLogIn),
							    ('/LogOut', LogOut),
							    ('/Settings', Settings),
							    
							    ('/KsuEditor', KsuEditor),
							    ('/SetViewer', SetViewer),

							    ('/EventHandler',EventHandler),

							    ('/PopulateRandomTheory',PopulateRandomTheory),
							    ('/DataStoreViewer',DataStoreViewer)
								], debug=True)

