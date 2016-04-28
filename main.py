#KASware V2.0.0 | Copyright 2016 Kasware Inc.

import webapp2, jinja2, os, re 


template_dir = os.path.join(os.path.dirname(__file__), 'html_files')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_html(self, template, **kw):
		t = jinja_env.get_template(template)
		return t.render(**kw)

	def print_html(self, template, **kw):
		self.write(self.render_html(template, **kw))


#----------


class SignUpLogIn(Handler):
    def get(self):
        self.print_html('SignUpLogIn.html')

    def post(self):
    	post_details = get_post_details(self)
    	user_action = post_details['action_description']
    	input_error = user_input_error(post_details)



    	if user_action == 'SignUp':
    		if input_error:
    			self.print_html('SignUpLogIn.html', post_details=post_details, input_error=input_error)

    		else:
    			self.write('Sing Up Successful!')
    			self.write(post_details)



    	if user_action == 'LogIn':
			self.write('Successful Log In')







class Home(Handler):
    def get(self):
        self.write('Ups! Seems like you are not logged in')





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



#--- Validation and security functions ----------


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
		'last_name_error': 'invalid first name syntax',
		
		'last_name': re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
		'last_name_error': 'invalid last name syntax',

		'password': re.compile(r"^.{3,20}$"),
		'password_error': 'invalid password syntax',
		
		'email': re.compile(r'^[\S]+@[\S]+\.[\S]+$'),
		'email_error': 'invalid email syntax'}





#----------

app = webapp2.WSGIApplication([
							    ('/', Home),
							    ('/SignUpLogIn', SignUpLogIn)
								], debug=True)
