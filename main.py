#KASware V2.0.0 | Copyright 2016 Kasware Inc.

import webapp2, jinja2, os 


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

    	if user_action == 'LogIn':
			self.write('Successful Log In')

    	if user_action == 'SignUp':
    		self.write('Sing Up Successful!')
    		self.write(post_details)





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



#----------

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/SignUpLogIn', SignUpLogIn)
	], debug=True)
