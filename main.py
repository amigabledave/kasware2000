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
			goal = theory.kpts_goals['typical_weekly_goals'][active_weekday]

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
						'minimum_daily_hours_of_fully_focus_effort':7}

				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					day_start_time=datetime.strptime('06:00', '%H:%M').time(),
					kpts_goals_parameters=kpts_goals_parameters,
					kpts_goals=calculate_user_kpts_goals(kpts_goals_parameters))

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

		self.print_html('KsuEditor.html', ksu=ksu, constants=constants)

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
			ksu = self.prepareInputForSaving(ksu, post_details)
			ksu.put()
		
		self.redirect(return_to)
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
		ksu_set = KSU.query(KSU.theory == user_key).order(KSU.created).fetch()
		self.print_html('TodaysMission.html', ksu_set=ksu_set, constants=constants, set_name='TodaysMission')


	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return

			
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

		event = Event(
			theory=self.theory.key,
			ksu_id =  KSU.get_by_id(int(event_details['ksu_id'])).key,
			event_type = event_details['user_action'],
			#Score properties
			user_date_ordinal=(datetime.today()-timedelta(hours=user_start_hour)).toordinal(),
			kpts_type = 'SmartEffort',
			duration = int(event_details['duration']),
			intensity = int(event_details['intensity']),
			score = int(event_details['duration'])*int(event_details['intensity']))		
		event.put()

		self.update_active_log(event)



		self.response.out.write(json.dumps({'mensaje':'Evento creado y guardado'}))
		return

	def update_active_log(self, event):
		active_log = self.active_log
		print
		print 'ya intento actualizar'
		print
		if event.kpts_type == 'SmartEffort':
			active_log.SmartEffort += event.score
			active_log.TotalScore += event.score
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

		theory_parameters = [
			[10, {'ksu_type':'KeyA', 'ksu_subtype':'KAS1'}]
		]

		for e in theory_parameters:
			set_size = e[0]
			set_details = e[1]

			ksu_subtype = constants['d_KsuSubtypes'][set_details['ksu_subtype']]

			for i in range(0, set_size):

				description =  ksu_subtype + 'no. ' + str(i) + ' of ' + username
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

	yearly_vacations_day = kpts_goals_parameters['yearly_vacations_day']
	yearly_shit_happens_days = kpts_goals_parameters['yearly_shit_happens_days']
	minimum_daily_hours_of_fully_focus_effort = kpts_goals_parameters['minimum_daily_hours_of_fully_focus_effort']
	
	typical_week_effort_distribution = kpts_goals_parameters['typical_week_effort_distribution']
	typical_week_active_days = sum(typical_week_effort_distribution)

	typical_day_minimum_effort = minimum_daily_hours_of_fully_focus_effort*60*3

	typical_week_minimum_effort = typical_day_minimum_effort*typical_week_active_days

	active_days = 365.25 - (yearly_vacations_day + yearly_shit_happens_days) - ((7 - typical_week_active_days) * (365.25/7.0))

	yearly_effort_goal = active_days * typical_day_minimum_effort

	daily_effort_consumption = yearly_effort_goal/365.25

	typical_weekly_goals = []
	for e in typical_week_effort_distribution:
		typical_weekly_goals.append(e * typical_day_minimum_effort)

	user_kpts_goals = {
		'typical_day_minimum_effort': math.ceil(typical_day_minimum_effort),
		'typical_week_minimum_effort': math.ceil(typical_week_minimum_effort),
		'daily_effort_consumption': math.ceil(daily_effort_consumption),
		'typical_weekly_goals': typical_weekly_goals
	}

	return user_kpts_goals





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

