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


class Home(Handler):
    def get(self):
        self.print_html('Home.html')



#----------

app = webapp2.WSGIApplication([
    ('/', Home)
], debug=True)
