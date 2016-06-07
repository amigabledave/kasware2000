#KASware V2.0.0 | Copyright 2016 Kasware Inc.
import webapp2, jinja2, os, re, random, string, hashlib 
from google.appengine.ext import ndb

from python_files import datastore, randomUser, constants

constants = constants.constants
Theory = datastore.Theory
KSU = datastore.KSU

template_dir = os.path.join(os.path.dirname(__file__), 'html_files')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_html(self, template, **kw):
		t = jinja_env.get_template(template)
		theory = self.theory 
		if theory:				
			return t.render(theory=theory,**kw)
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
		# if theory_id and Theory.get_by_theory_id(int(theory_id)): #Un intento de quitar el bouncer de todos los handlers
		# 	self.theory = Theory.get_by_theory_id(int(theory_id))
		# else:
		# 	self.redirect('/SignUpLogIn')




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
				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'])
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


class NewKSU(Handler):
	
	def get(self):
		if user_bouncer(self):
			return
		self.print_html('NewEditKSU.html', title='Define', ksu={}, constants=constants)

	def post(self):
		if user_bouncer(self):
			return
		post_details = get_post_details(self)
		user_action = post_details['action_description']
		
		if user_action == 'Create' or user_action == 'Create_Plus':
			# self.write(post_details)
			new_ksu = KSU(
				theory=self.theory.key,
				description=post_details['description'],
				repeats=post_details['repeats'])
			new_ksu.put()
			self.redirect('/')
			return			
				
		elif user_action == 'Discard':
			return



class Home(Handler):
    def get(self):
		if user_bouncer(self):
			return		
		theory = self.theory
		message = 'Welcome to KASware ' + theory.first_name + ' ' + theory.last_name
		self.write(message)
		




class TodaysMission(Handler):
	def get(self):
		if user_bouncer(self):
			return
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key).order(KSU.created).fetch()

		self.print_html('TodaysMission.html', ksu_set=ksu_set, constants=constants)


	def post(self):
		if user_bouncer(self):
			return

		post_details = get_post_details(self)
		user_action = post_details['action_description']	
		
		if user_action == 'NewKSU':
			self.redirect('/NewKSU')



class SetViewer(Handler):
	def get(self):
		if user_bouncer(self):
			return
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key).order(KSU.created).fetch()

		self.print_html('SetViewer.html', ksu_set=ksu_set, constants=constants)


	def post(self):
		if user_bouncer(self):
			return

		post_details = get_post_details(self)
		user_action = post_details['action_description']	
		
		if user_action == 'NewKSU':
			self.redirect('/NewKSU')

		if user_action == 'EditKSU':
			ksu_id = post_details['ksu_id']
			self.redirect('/EditKSU?ksu_id='+ksu_id)




class EditKSU(Handler):
	def get(self):
		if user_bouncer(self):
			return
		ksu_id = self.request.get('ksu_id')
		ksu = KSU.get_by_id(int(ksu_id)) #xx
		self.print_html('NewEditKSU.html', title='Define', ksu=ksu, constants=constants)






#--- Development handlers ----------

class PopulateRandomTheory(Handler):

	def populateRandomTheory(self, theorySize):
		theory = self.theory
		theory_key = theory.key
		username = theory.first_name + ' ' + theory.last_name
		for i in range(0, theorySize):
			description = 'KSU no. ' + str(i) + ' of ' + username
			new_ksu = KSU(
				theory=theory_key,
				description=description)
			new_ksu.put()		
		return
	
	def get(self):
		randomUserTheory = self.theory
		self.populateRandomTheory(5)
		self.redirect('/')



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


def user_bouncer(self):
	theory = self.theory
	if theory:
		return False
	else:
		self.redirect('/SignUpLogIn')
		return True


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




#----------

app = webapp2.WSGIApplication([
							    ('/', TodaysMission),
							    ('/SignUpLogIn', SignUpLogIn),
							    ('/LogOut', LogOut),
							    ('/NewKSU', NewKSU),
							    ('/EditKSU', EditKSU),
							    ('/SetViewer', SetViewer),

							    ('/PopulateRandomTheory',PopulateRandomTheory),
							    ('/DataStoreViewer',DataStoreViewer)
								], debug=True)

