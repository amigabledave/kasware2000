#KASware V2.0.0 | Copyright 2016 Kasware Inc.
# -*- coding: utf-8 -*-
import webapp2, jinja2, os, re, random, string, hashlib, json, logging, math 

from datetime import datetime, timedelta, time
from google.appengine.ext import ndb
from google.appengine.api import mail
from python_files import datastore, randomUser, constants, kasware_os


constants = constants.constants

Theory = datastore.Theory
KSU = datastore.KSU
Event = datastore.Event
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
		if theory:				
			return t.render(theory=theory, game=self.game, **kw)
		else:
			return t.render(**kw)

	def print_html(self, template, **kw):
		ksu_to_remember = {}
		current_objectives = []
		if self.theory:
			ksu_to_remember, current_objectives = get_ksu_to_remember(self)		

		self.write(self.render_html(template, ksu_to_remember=ksu_to_remember, current_objectives=current_objectives, **kw))

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
		self.game = self.theory and self.update_game()


	def update_game(self):

		def check_and_burn(theory, active_date,time_travel):
			
			game = theory.game 
			
			critical_burn = theory.game['critical_burn']

			user_key = theory.key

			today =(datetime.today()+timedelta(hours=theory.timezone)+timedelta(days=time_travel)) 
			today_ordinal = active_date
		
			burn_candidates = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False, KSU.in_graveyard == False, KSU.is_active == True, KSU.is_critical == True)

			burn_sets = ['KAS1', 'KAS2', 'EVPo', 'ImPe']

			for ksu in burn_candidates:

				if not ksu.next_event:
					ksu.next_event = today
					ksu.put()

				next_event = ksu.next_event.toordinal()

				if ksu.ksu_subtype in burn_sets and next_event < today_ordinal:

					next_critical_burn = ksu.next_critical_burn
					if not ksu.next_critical_burn or next_critical_burn < next_event:
						next_critical_burn = next_event
					
					kpts_burned = (today_ordinal - next_critical_burn) * critical_burn

					game['points_to_goal'] += kpts_burned
					ksu.next_critical_burn = today_ordinal
					ksu.put()

					event = Event(
						theory=self.theory.key,
						ksu_id =  ksu.key,
						event_type = 'Stupidity',
						user_date_date=today,
						user_date=today_ordinal,
						score = kpts_burned,
						
						comments = 'Critical burn',
						ksu_description = ksu.description,
						ksu_secondary_description = ksu.secondary_description,
						ksu_subtype = ksu.ksu_subtype, 
						ksu_tags = ksu.tags)
					event.put()

			return game				

		theory = self.theory
		time_travel = 0 #To be deleted. Time Travel aqui puedo hacer creer al programa que es otro dia
		active_date = (datetime.today()+timedelta(hours=theory.timezone)).toordinal() + time_travel # TT Time Travel aqui puedo hacer creer al programa que es otro dia

		game = theory.game
		last_log = game['last_log']

		
		if not last_log:
			last_log = active_date - 1

		if last_log < active_date:
			game = check_and_burn(theory, active_date, time_travel)
			kpts_to_survie = (active_date - last_log - 1) * game['daily_goal'] + game['points_to_goal']
			if kpts_to_survie <= game['piggy_bank']:
				game['streak'] += active_date - last_log
				game['piggy_bank'] -= kpts_to_survie
				if game['goal_achieved']:
					game['streak'] -= 1
			else:
				game['streak'] = 0
				game['piggy_bank'] = 0
			
			game['points_to_goal'] = game['daily_goal']
			game['goal_achieved'] = False
			game['last_log'] = active_date
			theory.game = game
			theory.put()

		return game




		
class SignUpLogIn(Handler):
	def get(self):
		self.print_html('SignUpLogIn.html', login_error = False)

	def post(self):
 
		post_details = json.loads(self.request.body)
		user_action = post_details['user_action']
		next_step = 'No next step defined'

		print
		print 'Asi se ve el AJAX Request'
		print post_details
		
		if user_action == 'Random_SignUp':
			post_details.update(randomUser.createRandomUser()) ## Creates a random user for testing purposes
		
		if user_action == 'SignUp' or user_action == 'Random_SignUp':
			input_error = user_input_error(post_details)
			theory = Theory.get_by_email(post_details['email'])	
			
			if input_error:
				next_step = 'TryAgain'
											
			elif theory:
				next_step = 'TryAgain'
				input_error = 'That email is already register to another user!'
				

			else:
				next_step = 'CheckYourEmail'
				password_hash = make_password_hash(post_details['email'], post_details['password'])
				
				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					timezone=-6,
					categories={'tags':[]})

				theory.put()

				#Loads OS Ksus
				for post_details in os_ksus:
					ksu = KSU(theory=theory.key)
					ksu = prepareInputForSaving(theory, ksu, post_details)
					ksu.put()
				
				# self.login(theory)				
				email_receiver = str(theory.email)
				# email_receiver = 'amigabledave@gmail.com'
				email_body = '<a href="kasware.com/Accounts?user_id='+str(theory.key.id())+'&user_request=validate_email">Confirm my account</a>' + ", I'm ready to start using KASware!"    			
				mail.send_mail(sender="KASware@kasware2000.appspotmail.com", to=email_receiver, subject="Please confirm your email address to start using KASware", body=email_body, html=email_body) #"<accounts@kasware.com>"
				print
				print email_body
				# self.redirect('/Accounts?user_request=create_account')
				# return
				# self.redirect('/MissionViewer?time_frame=Today')

			self.response.out.write(json.dumps({
				'next_step':next_step,
				'input_error':input_error
				}))
			return

		if user_action == 'LogIn':
			next_step = 'No next step defined'			
			email = post_details['email']
			password = post_details['password']
			theory = Theory.valid_login(email, password)
			if theory:
				self.login(theory)
				next_step = 'GoToYourTheory'
			else:
				next_step = 'TryAgain'
			
			self.response.out.write(json.dumps({
				'next_step':next_step,
				}))
			return


class Accounts(Handler):
	def get(self):
		
		theory_id = self.request.get('user_id')
		reset_code = self.request.get('reset_code')
		user_request = self.request.get('user_request')


		if theory_id:
			theory = Theory.get_by_theory_id(int(theory_id))
			
			if user_request == 'validate_email':
				if theory and not theory.valid_email:
					theory.valid_email = True
					theory.put()
					self.login(theory)
					self.redirect('/MissionViewer?time_frame=Today')
				else:
					self.redirect('/SignUpLogIn')

			else:
				self.print_html('Accounts.html', user_request=user_request, theory_id=theory_id, password_hash=reset_code)

		else:
			self.print_html('Accounts.html', user_request=user_request, theory_id=theory_id, password_hash=reset_code)


	def post(self):
		event_details = json.loads(self.request.body)
		user_action = event_details['user_action']
		next_step = 'No next step defined'

		if user_action == 'LogIn':					
			email = event_details['email']
			password = event_details['password']
			theory = Theory.valid_login(email, password)
			if theory:
				self.login(theory)
				next_step = 'GoToYourTheory'
			else:
				next_step = 'TryAgain'
			
			self.response.out.write(json.dumps({
				'next_step':next_step,
				}))
			return


		if user_action == 'RequestPasswordReset':
			theory = Theory.get_by_email(event_details['user_email'])	
			if theory:
				next_step = 'CheckYourEmail'

				email_receiver = str(theory.email)
				email_body = '<a href="kasware.com/Accounts?user_id='+str(theory.key.id())+'&user_request=set_new_password&reset_code='+str(theory.password_hash)+'">Reset my password</a>'
				mail.send_mail(sender="KASware@kasware2000.appspotmail.com", to=email_receiver, subject="KASware password reset", body=email_body, html=email_body) #"<accounts@kasware.com>"
				print
				print email_body

			else:
				next_step = 'EnterValidEmail'

			self.response.out.write(json.dumps({
				'next_step':next_step,
				}))
			return


		if user_action == 'SetNewPassword':
		
			theory_id = event_details['theory_id']
			reset_code = event_details['password_hash']
			print
			print 'Theory id:' + theory_id
			print 'Password hash: ' + reset_code

			theory = Theory.get_by_theory_id(int(theory_id))
			
			if reset_code == theory.password_hash:
				theory.password_hash = make_password_hash(theory.email, event_details['new_password'])
				theory.put()
				self.login(theory)
				next_step = 'GoToYourTheory'
			
			else:
				next_step = 'EnterValidPassword'

			self.response.out.write(json.dumps({
				'next_step':next_step,
				}))
			return


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

		user_today = local_today

		active_date = user_today.toordinal()
		
		tags = sorted(self.theory.categories['tags'])

		self.print_html('Settings.html', today=today, local_today=local_today, user_today=user_today, constants=constants, tags=tags)


	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		
		if user_action == 'SaveChanges':
			theory = self.theory
			game = self.game
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

	 		# if float(post_details['minimum_daily_effort']) != game['daily_goal']:
	 		# 	game['daily_goal'] = float(post_details['minimum_daily_effort'])
 			# 	game['piggy_bank'] = 0 
 			# 	game['streak'] = 0
 			# 	game['last_log'] = None
 			# 	game['goal_achieved'] = False
				# game['points_to_goal'] = game['daily_goal']
 			
			game['critical_burn'] = int(post_details['critical_burn'])
			game['daily_goal'] = int(post_details['minimum_daily_effort'])
 			game['piggy_bank'] = int(post_details['piggy_bank'])
 			game['streak'] = int(post_details['streak'])
 			
 			theory.game = game
	 		theory.put()

 		self.redirect('/MissionViewer?time_frame=Today')


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
		ksu_id = self.request.get('ksu_id')
		set_title = constants['d_SetTitles'][set_name]
		parent_id = ''
		dreams = []
		objectives = []
		view_type = ''

		if not set_name:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False).order(KSU.importance).order(KSU.created).fetch()
		
		elif set_name == 'TheoryQuery':
			lookup_string = self.request.get('lookup_string')
			user_theory = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.is_deleted == False).order(KSU.importance).order(KSU.created).fetch() 
			# user_theory = KSU.query(KSU.theory == user_key ).order(KSU.importance).order(KSU.created).fetch() #TBD
			ksu_set = self.search_theory(user_theory, lookup_string)
			set_title = 'You searched for: ' + lookup_string
		
		elif set_name == 'Graveyard':
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == True, KSU.is_deleted == False).order(KSU.importance).order(KSU.created).fetch()

		elif ksu_id:			
			ksu = KSU.get_by_id(int(ksu_id))
			ksu_key = ksu.key			
			ksu_set = KSU.query(KSU.parent_id == ksu_key).filter(KSU.is_deleted == False).order(KSU.importance).order(KSU.created).fetch()
			set_title = ksu.description
			parent_id = int(ksu_id)
			dreams = self.get_active_dreams(user_key)
			objectives = self.get_user_objectives(user_key)
			# if set_name == 'BOKA':				
				# objectives, big_objectives = self.get_user_objectives(user_key)
				# objectives = self.get_user_objectives(user_key)
			view_type ='Plan'
		
		else:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.ksu_type == set_name).order(KSU.ksu_subtype).order(-KSU.is_active).order(KSU.importance).order(KSU.created)

			if self.theory.hide_private_ksus:
				ksu_set = ksu_set.filter(KSU.is_private == False)
		
			if set_name == 'BigO':				
				ksu_set = ksu_set.filter(KSU.ksu_subtype == 'BigO')
				# objectives, big_objectives = self.get_user_objectives(user_key)
				objectives = self.get_user_objectives(user_key)
				dreams = self.get_active_dreams(user_key)

			if set_name == 'KeyA':				
				objectives = self.get_user_objectives(user_key)
				dreams = self.get_active_dreams(user_key)



			ksu_set = ksu_set.fetch()
		

		for ksu in ksu_set:
			ksu.description_rows = determine_rows(ksu.description)
			ksu.secondary_description_rows = determine_rows(ksu.secondary_description)
			ksu.comments_rows = determine_rows(ksu.comments)


		new_ksu_required_templates = []
		ksu = constants['ksu_for_template']			
		for ksu_subtype in constants['type_to_subtypes'][set_name]:
			template = ksu.copy()
			template['ksu_subtype'] = ksu_subtype
			template['ksu_type'] = set_name
			new_ksu_required_templates.append(template)	

		
		tags = self.theory.categories['tags'] # por el quick adder
		ksu_set, set_tags, wish_type_definitions = self.get_set_tags(ksu_set, set_name)
		self.print_html(
			'SetViewer.html', 
			new_ksu_required_templates=new_ksu_required_templates, 
			viewer_mode='Set',  
			ksu_set=ksu_set, 
			constants=constants, 
			set_name=set_name, 
			ksu={}, 
			tags=tags, 
			set_title=set_title, 
			parent_id=parent_id, 
			dreams=dreams, 
			objectives=objectives, 
			view_type=view_type, 
			set_tags=set_tags, 
			wish_type_definitions=wish_type_definitions) #

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
			
			ksu_description = remplaza_acentos(ksu.description).lower() + ' ' + remplaza_acentos(ksu.secondary_description).lower() + ' ' + remplaza_acentos(ksu.tags).lower() + str(ksu.key.id()) #Hace que tambien sea posible buscar un KSU por id

			if ksu_description.find(lookup_string) != -1:
				main_result.append(ksu)
			else:
				for word in lookup_words:
					if ksu_description.find(word) != -1 and ksu not in secondary_result:
						secondary_result.append(ksu)

		return main_result + secondary_result

	def get_active_dreams(self, user_key):
		ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.ksu_type == 'Wish', KSU.is_critical == True).order(-KSU.is_active).order(KSU.importance).order(KSU.created)
		dreams = []
		for ksu in ksu_set:
			dreams.append((ksu.key.id(), ksu.description))
		return dreams

	def get_user_objectives(self, user_key):
		ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.ksu_type == 'BigO').order(-KSU.is_active).order(KSU.importance).order(KSU.created)
		# objectives = [(None,'-- None --')]
		big_objectives = []
		for ksu in ksu_set:
			big_objectives.append((ksu.key.id(), ksu.description))
			# if ksu.ksu_subtype == 'BigO':				
			# 	objectives.append((ksu.key.id(), ksu.description))
			# 	big_objectives.append((ksu.key.id(), ksu.description))
			# else:
			# 	objectives.append((ksu.key.id(), ksu.description))
		return big_objectives #,objectives


	def remove_inactive_child_objectives(self, objectives):
		result = []
		for ksu in objectives:
			if not ksu.parent_id:
				result.append(ksu)
			elif ksu.is_active:
				result.append(ksu)
		return result

	#xx
	def get_set_tags(self, ksu_set, set_name):
		set_tags = []
		for ksu in ksu_set:
			if ksu.tags and ksu.tags != 'NoTags':
				ksu_tags = (ksu.tags).replace(', ',',').split(',')
				for tag in ksu_tags:
					if tag not in set_tags:
						set_tags.append(tag)
			else:
				ksu.tags = 'NoTags'

		set_tags = ['NoTags'] + sorted(set_tags)
		tags_tuples = []
		i = 0
		for tag in set_tags:
			tags_tuples.append(('TagId_' + str(i),tag))
			i += 1

		wish_type_definitions = None
		if set_name in ['Wish', 'RTBG']:
			wish_tags = {'doing':['NoTags'], 'having':['NoTags'], 'being':['NoTags'], 'achieving':['NoTags']}
			wish_tuples = {'doing':[], 'having':[], 'being':[], 'achieving':[]}

			for ksu in ksu_set:
				if ksu.tags != 'NoTags':
					set_tags = wish_tags[ksu.wish_type]
					ksu_tags = (ksu.tags).replace(', ',',').split(',')
					for tag in ksu_tags:
						if tag not in set_tags:
							set_tags.append(tag)
					wish_tags[ksu.wish_type] = set_tags

			i = 0	
			for wish_type in ['doing', 'having', 'being', 'achieving']:
				wish_type_tags_tuples = []
				set_tags = wish_tags[wish_type]		
				for tag in set_tags:
					wish_type_tags_tuples.append(('TagId_' + str(i),tag))
					i += 1
				wish_tuples[wish_type] = wish_type_tags_tuples

			tags_tuples = wish_tuples

			if set_name == 'Wish':
				wish_type_definitions = [['doing', 'Experiencing'], ['having', 'Having'], ['being', 'Being'], ['achieving', 'Achieving']]
			elif set_name == 'RTBG':
				wish_type_definitions = [['doing', 'Experience'], ['having', 'Having/Have had'], ['being', 'Being/Had been'], ['achieving', 'Achievement']]

		print
		print 'These are the tags tuples'
		print tags_tuples
		print


		return ksu_set, tags_tuples, wish_type_definitions 


class MissionViewer(Handler):

	@super_user_bouncer
	def get(self):
		time_frame = self.request.get('time_frame')

		tags = self.theory.categories['tags']		
		full_mission, objectives, today, dreams = self.generate_todays_mission(time_frame)
				
		if time_frame == 'Today':
			time_frame_sets = ['kick_off', 'anywhere_anytime','today','wrap_up']
		else:
			time_frame_sets = ['tomorrow', 'this_week', 'this_month', 'later', 'someday_maybe']


		new_ksu_required_templates = []
		for ksu_subtype in ['KAS2']:
			ksu = constants['ksu_for_template']
			ksu['ksu_subtype'] = ksu_subtype
			new_ksu_required_templates.append(ksu)
	


		self.print_html('MissionViewer.html',
						viewer_mode='Mission', 
						full_mission=full_mission,
						objectives=objectives,
						dreams=dreams,
						time_frame_sets=time_frame_sets,
						time_frame=time_frame,
	
						reactive_mission=full_mission['timeless_reactive']['horizon_set'],

						constants=constants,
						today=today,
						tags=tags,
						new_ksu_required_templates=new_ksu_required_templates)

	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):
		return


	def generate_todays_mission(self, time_frame):

		theory = self.theory
		user_key = theory.key

		today =(datetime.today()+timedelta(hours=theory.timezone)).date() 
		today_ordinal =(datetime.today()+timedelta(hours=theory.timezone)).date().toordinal()
	
		current_time = (datetime.today()+timedelta(hours=theory.timezone)).time()

		ksu_set = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False, KSU.in_graveyard == False, KSU.is_active == True)

		if theory.hide_private_ksus:
			ksu_set = ksu_set.filter(KSU.is_private == False)
		
		if time_frame == 'Upcoming':
			ksu_set = ksu_set.order(-KSU.is_critical).order(KSU.next_event).order(KSU.importance).order(KSU.best_time).fetch()
		else:
			ksu_set = ksu_set.order(KSU.importance).order(-KSU.is_critical).order(KSU.best_time).fetch()

		full_mission = {

			'timeless_reactive':{
				'horizon_title':'Reactive Mission',
				'horizon_set':[]},

			'hidden_reactive':{
				'horizon_title':'Reactive Mission',
				'horizon_set':[]},

			'kick_off':{
				'horizon_title':'Kick Off',
				'horizon_set':[]},

			'anywhere_anytime':{
				'horizon_title':'Anywhere Anytime',
				'horizon_set':[]},

			'wrap_up':{
				'horizon_title':'Wrap Up',
				'horizon_set':[]},


			'today':{
				'horizon_title':'Actions to execute',
				'horizon_set':[]},
		 	
		 	'tomorrow':{
		 		'horizon_title':'Tomorrow',
				'horizon_set':[]},
			
			'this_week':{
				'horizon_title':'This Week',
				'horizon_set':[]},
			
			'this_month':{
				'horizon_title':'This Month',
				'horizon_set':[]},
			
			'later':{
				'horizon_title':'Later',
				'horizon_set':[]},
		 	
		 	'someday_maybe':{
		 		'horizon_title':'Someday... maybe',
				'horizon_set':[]},

			'hidden_someday_maybe':{
		 		'horizon_title':'Joy Generators Someday ... maybe',
				'horizon_set':[]}}


		def define_horizon(ksu, today_ordinal):
			next_event = ksu.next_event

			if not next_event:
				if ksu.ksu_type in ['BOKA']:
					return 'hidden_someday_maybe'
				else:
					return 'someday_maybe'

			next_event = next_event.toordinal()
			mission_view = ksu.mission_view

			if ksu.ksu_subtype in ['KAS3', 'KAS4']:
				if next_event <= today_ordinal:					
					if mission_view == 'KickOff':
						return 'kick_off'

					elif mission_view == 'AnywhereAnytime':
						return 'anywhere_anytime'

					elif mission_view == 'WrapUp':
						return 'wrap_up'

					else:				
						return 'timeless_reactive'
				else:
					return 'hidden_reactive'


			if next_event <= today_ordinal:
				if mission_view == 'KickOff':
					return 'kick_off'

				elif mission_view == 'AnywhereAnytime':
					return 'anywhere_anytime'

				elif mission_view == 'WrapUp':
					return 'wrap_up'

				else:				
					return 'today'


			if next_event - 1 <= today_ordinal:
				return 'tomorrow'

			if next_event - 7 <= today_ordinal:
				return 'this_week'

			if next_event - 30 <= today_ordinal:
				return 'this_month'

			else:
				return 'later'


		objectives = []
		dreams = []

		mission_sets = ['KAS1', 'KAS2', 'KAS3', 'KAS4', 'EVPo', 'ImPe', 'RealitySnapshot', 'BinaryPerception', 'TernaryPerception','FibonacciPerception', 'Diary']
		
		for ksu in ksu_set:
			mission_view = ksu.mission_view
			ksu_subtype = ksu.ksu_subtype
	
			next_event = ksu.next_event
			ksu.description_rows = determine_rows(ksu.description)
			ksu.secondary_description_rows = determine_rows(ksu.secondary_description)

			if ksu.parent_id:
				ksu.parent_id_id = ksu.parent_id.id()

			if ksu_subtype in mission_sets:
				time_horizon = define_horizon(ksu, today_ordinal)
				full_mission[time_horizon]['horizon_set'].append(ksu)
				## Apendix - TBD
				# if not ksu.kpts_value:
				# 	ksu.kpts_value = 0
				#				

			elif ksu_subtype == 'BigO':
				objectives.append((ksu.key.id(), ksu.description))

			elif ksu_subtype == 'Wish' and ksu.is_critical:
				dreams.append((ksu.key.id(), ksu.description))
			

		return full_mission, objectives, today , dreams 


class EventHandler(Handler):
	
	@super_user_bouncer
	def post(self):
			
		event_details = json.loads(self.request.body)

		print
		print 'Si llego el AJAX Request. User action: ' +  event_details['user_action'] + '. Event details: ' +  str(event_details)
		print  event_details['user_action']

		user_action = event_details['user_action']

		
		if user_action == 'UpdateSettingsTag':
			self.update_tags_from_settings(event_details['original_tag'], event_details['new_tag'])
			return

		if user_action == 'SaveNewKSU':			
			ksu = KSU(theory=self.theory.key)
			
			if not 'is_active' in event_details:
				event_details['is_active'] = True

			new_event_details = event_details.copy()
			for a_key in event_details:
				a_val = event_details[a_key]
				if a_val == '':
					del new_event_details[a_key]

			ksu = prepareInputForSaving(self.theory, ksu, new_event_details)
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
			
			event = Event.get_by_id(int(event_details['event_id']))
			kpts_type = event.kpts_type
			score = event.score

			## Desde aqui empieza la nueva forma de actualizar para game
			game = self.game

			if kpts_type == 'Stupidity':
				game['piggy_bank'] += score
				
			elif kpts_type == 'SmartEffort':
				game['points_to_goal'] += score			
			
			theory = self.theory
			theory.game = game
			theory.put()
			#
 			
			event.is_deleted = True
			event.put()
			
			ksu = KSU.get_by_id(event.ksu_id.id())
			ksu.in_graveyard = False
			ksu.is_deleted = False
			today =(datetime.today()+timedelta(hours=self.theory.timezone))
			ksu.next_event = today
			ksu.put()

			self.response.out.write(json.dumps({
				'mensaje':'Evento revertido',
				'PointsToGoal': game['points_to_goal'],
				'EffortReserve': game['piggy_bank'],
				'Streak': game['streak']})) 
			return

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

		if user_action == 'TimerStop':
			ksu = KSU.get_by_id(int(event_details['ksu_id']))
			ksu.timer['hours'] =  int(event_details['hours'])
			ksu.timer['minutes'] =  int(event_details['minutes'])
			ksu.timer['seconds'] =  int(event_details['seconds'])
			ksu.timer['value'] =  event_details['timer_value']
			ksu.kpts_value =  float(event_details['kpts_value'])
			ksu.put()
			return

		ksu = KSU.get_by_id(int(event_details['ksu_id']))
		ksu_subtype = ksu.ksu_subtype
		
		event = Event(
			theory=self.theory.key,
			ksu_id =  ksu.key,
			parent_id=ksu.parent_id,
			event_type = user_action,
			user_date_date=(datetime.today()+timedelta(hours=self.theory.timezone)),
			user_date=(datetime.today()+timedelta(hours=self.theory.timezone)).toordinal(),
			
			comments = event_details['event_comments'].encode('utf-8'),
			secondary_comments = event_details['event_secondary_comments'].encode('utf-8'),
			ksu_description = ksu.description,
			ksu_secondary_description = ksu.secondary_description,
			ksu_subtype = ksu.ksu_subtype, 
			ksu_tags = ksu.tags)
		
		# print 'Este es el tipo de KSU al que corresponde'
		# print ksu_subtype

		if ksu.ksu_type in ['ImIn', 'Diary'] and ksu.next_event.toordinal() < event.user_date:
			user_date = ksu.next_event.toordinal()
			event.user_date_date = datetime.fromordinal(user_date) + timedelta(hours=23) + timedelta(minutes=59)
			event.user_date = user_date

		if user_action == 'RecordValue':
			event.kpts_type = 'IndicatorValue'
			event.score = float(event_details['kpts_value'])
			
			if 'is_private' in event_details:
				event.is_private = event_details['is_private']
			
			if 'importance' in event_details:
				event.importance = int(event_details['importance'])

			update_next_event(self, user_action, {}, ksu)
			event.put()	

		if user_action in ['MissionDone', 'ViewerDone']:

			if ksu_subtype in ['KAS1', 'KAS2', 'KAS3', 'KAS4', 'EVPo', 'ImPe']:
				event.kpts_type = 'SmartEffort'
				event.score = float(event_details['kpts_value'])
				
				if ksu_subtype == 'KAS2':
					if ksu.is_mini_o:
						# print 'Si se dio cuenta de que es un MiniO'
						ksu.secondary_description = None
						ksu.best_time = None
						ksu.kpts_value = 1
					else:
						ksu.is_deleted = True

				update_next_event(self, user_action, {}, ksu)

				if ksu_subtype in ['EVPo']:
					event.quality = event_details['event_quality']


				ksu.timer['hours'] =  0
				ksu.timer['minutes'] =  0
				ksu.timer['seconds'] =  0
				ksu.timer['value'] =  '00:00:00'

			
			if ksu_subtype == 'KAS4':
				event.kpts_type = 'Stupidity'
				event.score = float(event_details['kpts_value'])				

			if ksu_subtype == 'BigO':
				event.kpts_type = 'Achievement'				
				ksu.in_graveyard = True

			if ksu_subtype == 'Wish':				
				event.kpts_type = 'Achievement'				
				ksu.in_graveyard = True
				event.quality = event_details['event_quality']
				
			self.update_active_log(event)
			event.put()


		if user_action in ['MissionPush', 'SendToMission']:			
			update_next_event(self, user_action, {}, ksu)
			

		if user_action == 'MissionSkip':
			if ksu_subtype == 'KAS3':
				event.kpts_type = 'Stupidity'
				event.score = float(self.theory.game['critical_burn'])
				self.update_active_log(event)
				event.put()	
			else:	
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
		

		# print
		# print 'Este fue el evento que se creo: '
		# print event

		game = self.game

		event_id = None
		if event.key:
			event_id = event.key.id()

		self.response.out.write(json.dumps({'mensaje':'Evento creado y guardado',
											'event_id':event_id ,
											'pretty_event_date':event.user_date_date.strftime('%a, %b %d, %Y'), 
											
											'event_comments':event.comments,
											'EventScore':event.score, 											
											'kpts_type':event.kpts_type, 
											
											'ksu_subtype':ksu_subtype, 
											'kpts_value':ksu.kpts_value,
											'pretty_next_event':ksu.pretty_next_event,
											'is_active':ksu.is_active,
											
											'PointsToGoal':game['points_to_goal'],
											'EffortReserve':game['piggy_bank'],
											'Streak':game['streak']}))
		return


	def update_active_log(self, event):

		game = self.game

		minimum_daily_effort = game['daily_goal']

		if event.kpts_type == 'SmartEffort':
			if  game['points_to_goal'] == 0:
				game['piggy_bank'] += event.score
			
			elif event.score >= game['points_to_goal']:
				game['piggy_bank'] += event.score - game['points_to_goal'] 
 				game['points_to_goal'] = 0
 				if not game['goal_achieved']:
	 				game['goal_achieved'] = True
	 				game['streak'] += 1

 			else: 				 
 				game['points_to_goal'] -= event.score

		if event.kpts_type == 'Stupidity':
			game['points_to_goal'] += event.score

		theory = self.theory
		theory.game = game
		theory.put()


	def update_single_attribute(self, ksu, attr_key, attr_value):
		updated_value = None
		
		if attr_key in ['description', 'secondary_description', 'comments', 'repeats', 'secondary_comments','mission_view', 'wish_type']:
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
				if ksu.ksu_subtype not in ['KAS1', 'EVPo', 'ImPe']:
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

		elif attr_key in ['importance', 'frequency', 'effort_denominator']:
			setattr(ksu, attr_key, int(attr_value))	
			updated_value = int(attr_value)

		elif attr_key in ['is_critical', 'is_private', 'is_active', 'is_mini_o']:
			if attr_value == 'on':
				attr_value = True
			setattr(ksu, attr_key, attr_value)

		elif attr_key in ['repeats_on_Mon', 'repeats_on_Tue', 'repeats_on_Wed', 'repeats_on_Thu', 'repeats_on_Fri', 'repeats_on_Sat', 'repeats_on_Sun']:
			ksu.repeats_on[attr_key] = attr_value 

		elif attr_key == 'parent_id':

			if attr_value == 'None':
				ksu.parent_id = None
				if ksu.ksu_type == 'BOKA':
					ksu.ksu_type = 'KAS2'
			else:	
				parent_ksu = KSU.get_by_id(int(attr_value))
				ksu.parent_id = parent_ksu.key
				if ksu.ksu_subtype == 'KAS2':
					ksu.ksu_type = 'BOKA'

		elif attr_key in ['money_cost', 'days_cost', 'hours_cost']:
			ksu.cost[attr_key] = int(attr_value)


		ksu.put()	
		return updated_value


	def update_tags_from_settings(self, original_tag, new_tag):	
		theory = self.theory
		current_tags = self.theory.categories['tags']
		new_tag = prepare_new_tag_for_saving(new_tag)
		new_tags = replace_in_list(current_tags, original_tag, new_tag)
		theory.categories['tags'] = new_tags
		theory.put()		

		ksu_set = KSU.query(KSU.theory == theory.key ).fetch()
		
		print 'los originales'
		print original_tag
		print new_tag

		for ksu in ksu_set:
			tags_string = ksu.tags			
			print
			print tags_string
			print tags_string and original_tag in tags_string			 

			if tags_string and original_tag in tags_string:
				tags_string = tags_string.replace(', ',',')							
				print tags_string
				new_tags_string = ''
				ksu_tags = tags_string.split(',')
				print ksu_tags

				
				i = len(ksu_tags)
				if i == 1 and new_tag == '':
					ksu.tags = None
					ksu.put()
					return
				
				for tag in ksu_tags:
					i -= 1
					if tag == original_tag:
						if new_tag != '':
							new_tags_string += new_tag
							if i > 0:
								new_tags_string += ', '
					else:
						new_tags_string += tag
						if i > 0:
							new_tags_string += ', '

				ksu.tags = new_tags_string
				ksu.put()
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

		today =(datetime.today()+timedelta(hours=self.theory.timezone)).date().toordinal()
		pretty_today = (datetime.today()+timedelta(hours=self.theory.timezone)).date().strftime('%a, %b %d, %Y')

		history_start = self.request.get('history_start')
		if history_start:
			history_start = int(history_start) - 1
		elif ksu_id:
			history_start = (self.theory.created).toordinal() - 1
		else:
			history_start = today - 1

		history_end = self.request.get('history_end')
		if history_end:
			history_end = int(history_end)
		else:
			history_end = today

		history, history_value = self.retrieve_history(ksu_id, history_start, history_end)
		history_start = datetime.fromordinal(history_start)
		history_end = datetime.fromordinal(history_end)

		self.print_html('HistoryViewer.html', diary_view=diary_view, history_title=history_title, history=history, history_start=history_start, history_end=history_end, history_value=history_value, constants=constants, pretty_today=pretty_today, ksu_id=ksu_id)


	@super_user_bouncer
	@CreateOrEditKSU_request_handler	
	def post(self, user_action, post_details):

		redirect_to = '/HistoryViewer'

		today =(datetime.today()+timedelta(hours=self.theory.timezone)).date().toordinal()

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

	def retrieve_history(self, ksu_id, history_start, history_end):
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
		
		history = []
		history_value = 0

		for event in event_set:
			ksu = KSU.get_by_id(event.ksu_id.id())
			
			event.pretty_date = (event.user_date_date).strftime('%I:%M %p. %a, %b %d, %Y')
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
				

				theory = Theory(
					email=post_details['email'], 
					password_hash=password_hash, 
					first_name=post_details['first_name'], 
					last_name=post_details['last_name'],
					timezone=-6,
					categories={'tags':[]})

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

		today =(datetime.today()+timedelta(hours=theory.timezone))
		print
		print 'Este es el today de PopulateTheory:'
		print today

		theory_parameters = [
			[3	,{'ksu_type':'Gene', 'ksu_subtype':'Gene'}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS1', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':2, 'frequency':1, 'repeats':'R001'}],
			[3, {'ksu_type':'OTOA', 'ksu_subtype':'KAS2', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':3}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS3', 'kpts_value':0.25}],
			[3, {'ksu_type':'KeyA', 'ksu_subtype':'KAS4', 'kpts_value':5}],
			[3, {'ksu_type':'BigO', 'ksu_subtype':'BigO'}],
			[3, {'ksu_type':'Wish', 'ksu_subtype':'Wish'}],
			[3, {'ksu_type':'EVPo', 'ksu_subtype':'EVPo', 'next_event':today, 'kpts_value':1, 'frequency':7}],
			[3, {'ksu_type':'ImPe', 'ksu_subtype':'ImPe', 'next_event':today, 'kpts_value':0.25, 'frequency':30}],
			[3, {'ksu_type':'Idea', 'ksu_subtype':'Idea'}],
			[3, {'ksu_type':'RTBG', 'ksu_subtype':'RTBG'}],
			[1, {'ksu_type':'Diary', 'ksu_subtype':'Diary', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'RealitySnapshot', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'BinaryPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[1, {'ksu_type':'ImIn', 'ksu_subtype':'TernaryPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],			
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


def update_next_event(self, user_action, post_details, ksu):

	def days_to_next_event(ksu):

		if ksu_subtype in ['EVPo']:
			return ksu.frequency

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

			today =(datetime.today()+timedelta(hours=self.theory.timezone))

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
	
	print 'Este es el tipo de KSU que se esta intentado actualizar el evento'
	print ksu.ksu_subtype

	today =(datetime.today()+timedelta(hours=self.theory.timezone))
	tomorrow = today + timedelta(days=1)
	ksu_subtype = ksu.ksu_subtype	
	
	if ksu_subtype in ['KAS1', 'EVPo']:
		next_event = ksu.next_event
		days_to_next_event = days_to_next_event(ksu)
		print
		print 'Si quiere actualizar el evento'


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

	elif ksu_subtype in ['KAS2']:

		if user_action in ['MissionDone', 'ViewerDone'] and not ksu.is_mini_o:
			ksu.next_event = None
			ksu.pretty_next_event = None

		if user_action == 'MissionSkip':
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

		print
		print 'Hasta aqui ya llego a darse cuenta que es KAS3 o KAS4 '
		

		if user_action in ['MissionDone']:
			if ksu.mission_view == 'Principal':
				ksu.next_event = today
				ksu.pretty_next_event = today.strftime('%a, %b %d, %Y')
			else:
				ksu.next_event = tomorrow
				ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')


	elif ksu_subtype in ['ImPe', 'RealitySnapshot', 'FibonacciPerception', 'TernaryPerception', 'BinaryPerception', 'Diary']:
		
		next_event = ksu.next_event

		if not next_event:
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')
		
		if user_action in ['MissionDone', 'MissionSkip', 'ViewerDone', 'RecordValue']:
			ksu.next_event += timedelta(days=ksu.frequency)
			ksu.pretty_next_event = (next_event + timedelta(days=ksu.frequency)).strftime('%a, %b %d, %Y')

		if user_action == 'MissionPush':
			ksu.next_event = tomorrow
			ksu.pretty_next_event = tomorrow.strftime('%a, %b %d, %Y')

		if user_action == 'SendToMission':
			ksu.next_event = today
			ksu.pretty_next_event = (today).strftime('%a, %b %d, %Y')

	return		

def prepareInputForSaving(theory, ksu, post_details):

	def determine_ksu_subtype(ksu, post_details):

		ksu_type = ksu.ksu_type

		if 'ksu_subtype' in post_details:
			ksu_subtype = post_details['ksu_subtype']
		else:
			ksu_subtype = ksu_type

		if ksu_type in ['OTOA', 'BOKA']:
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
			print 
			print 'Este es el tipo de attributo que quiero actualizar'
			print a_type
		
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


		if a_type == 'dict_cost':
			ksu.cost[a_key] = int(a_val)
		

		if a_type =='user_tags':
			a_val, tags = prepare_tags_for_saving(a_val)
			setattr(ksu, a_key, a_val.encode('utf-8'))
			update_user_tags(theory, tags)
			theory.categories['tags'] = update_user_tags(theory, tags)
			theory.put()

		if a_type == 'parent_id':
			if a_val == 'None':
				ksu.parent_id = None
			else:			
				parent_ksu = KSU.get_by_id(int(a_val))
				parent_key = parent_ksu.key
				ksu.parent_id = parent_key
				# if post_details['ksu_type'] != 'BigO': #Segun yo esto esta mal
				if parent_ksu.ksu_type == 'BigO': #Creo que esto es mas correcto
					ksu.ksu_type = 'BOKA'

	setattr(ksu, 'repeats_on', d_repeats_on)
	
	ksu.ksu_subtype = determine_ksu_subtype(ksu, post_details)

	if ksu.ksu_subtype == 'ImPe' and not ksu.secondary_description:
		ksu.secondary_description = 'Contact ' + ksu.description

	if ksu.ksu_subtype in ['KAS1','KAS3','KAS4','ImPe', 'RealitySnapshot', 'Diary', 'FibonacciPerception', 'TernaryPerception', 'BinaryPerception'] and not ksu.next_event:
		ksu.next_event = datetime.today() ## - timedelta(days=1) #Esto tenia una logica, pero por el momento se lo quito 

	if ksu.ksu_subtype in ['KAS1','KAS3','KAS4','ImPe', 'RealitySnapshot', 'Diary', 'FibonacciPerception', 'TernaryPerception', 'BinaryPerception'] and not ksu.frequency:
		ksu.frequency = 1

	if ksu.ksu_subtype == 'MiniO':
		ksu.ksu_type = 'BigO'

	print
	print 'Este es el nuevo sub tipo de KSU que estoy creando'
	print ksu.ksu_type
	print ksu.ksu_subtype

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
	tags_string = tags_string.replace(', ',',')
	valid_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ','&','!','_','-',',','.','1','2','3','4','5','6','7','8','9','0']
	clean_tags_string = ''
	for i in range(0,len(tags_string)):
		character = tags_string[i]
		if character in valid_characters:
			clean_tags_string += character
	tags = clean_tags_string.split(',')
	final_tags_string = tags_string.replace(',',', ')
	return final_tags_string, tags

def prepare_new_tag_for_saving(new_tag):

	tags_string = remplaza_acentos(new_tag)
	tags_string = tags_string.replace(', ',',')
	valid_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ','&','!','_','-','.','1','2','3','4','5','6','7','8','9','0']
	clean_tags_string = ''
	for i in range(0,len(tags_string)):
		character = tags_string[i]
		if character in valid_characters:
			clean_tags_string += character
	return clean_tags_string

def replace_in_list(target_list, old_value, new_value):
	new_list = []
	for e in target_list:
		if e == old_value: 
			if new_value !='':
				new_list.append(new_value)
		else:
			new_list.append(e)
	return new_list

def update_user_tags(theory, tags):

	current_tags = theory.categories['tags']
	for tag in tags:
		if tag not in current_tags:
			current_tags.append(tag)
	return sorted(current_tags)
	
def determine_rows(ksu_description):
	if not ksu_description:
		return 1
	return int(math.ceil((len(ksu_description)/70.0)))

def get_ksu_to_remember(self):
	
	theory = self.theory
	user_key = theory.key

	today =(datetime.today()+timedelta(hours=theory.timezone)).date()
	today_ordinal =(datetime.today()+timedelta(hours=theory.timezone)).date().toordinal()


	sets_to_remember = ['Idea', 'Wish', 'RTBG']
	ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.is_active == True).order(KSU.times_reviewed).order(KSU.importance).order(KSU.created)

	if self.theory.hide_private_ksus:
		ksu_set = ksu_set.filter(KSU.is_private == False)

	ksu_set = ksu_set.fetch()
	filtered_ksu_set = []
	current_objectives = []
	milestones = []
	objectives = []

	for ksu in ksu_set:
		ksu_type = ksu.ksu_type
		if ksu_type in sets_to_remember:
			filtered_ksu_set.append(ksu)
		elif ksu_type == 'BigO':
			if ksu.ksu_subtype == 'BigO':
				if ksu.next_event:
					ksu.days_left = '-- ' + str((ksu.next_event).toordinal() - today_ordinal) + ' days left --'
				else:
					ksu.days_left = '-- ??? days left --'

				if ksu.parent_id:
					ksu.parent_description = (KSU.get_by_id(ksu.parent_id.id())).description
				else:
					ksu.parent_description = None				
				current_objectives.append(ksu)
			elif ksu.ksu_subtype == 'MiniO':
				milestones.append(ksu)

	for BigO in current_objectives:
		BigO_id = BigO.key.id()
		BigO.milestones = []
		BigO.milestones_len = 0
		for milestone in milestones:
			if milestone.parent_id and milestone.parent_id.id() == BigO_id:
				BigO.milestones.append(milestone.description)
				BigO.milestones_len += 1



	if filtered_ksu_set:
		ksu_less_reviewed = filtered_ksu_set[0]
		ksu_less_reviewed.times_reviewed += 1
		ksu_less_reviewed.put()
	else:
		ksu_less_reviewed = {}

	return ksu_less_reviewed, current_objectives
	


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
		'first_name_error': 'Invalid first name. Your first name most be at least 3 charachers long and cannot contain any special characters.',
		
		'last_name': re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
		'last_name_error': 'Invalid last name. Your first name most be at least 3 charachers long and cannot contain any special characters.',

		'password': re.compile(r"^.{8,20}$"),
		'password_error': 'Invalid password. Your password most be at least 8 characters long.',
		
		'email': re.compile(r'^[\S]+@[\S]+\.[\S]+$'),
		'email_error': 'Invalid email syntax.'}



#--- Request index
app = webapp2.WSGIApplication([
							    ('/', SetViewer),
							    ('/SignUpLogIn', SignUpLogIn),
							    ('/Accounts', Accounts),
							    ('/LogOut', LogOut),
							    ('/Settings', Settings),
							    
							    ('/KsuEditor', KsuEditor),
							    ('/MissionViewer', MissionViewer),
							    ('/SetViewer', SetViewer),
						
							    ('/EventHandler',EventHandler),
							    ('/HistoryViewer', HistoryViewer),

							    ('/PopulateRandomTheory',PopulateRandomTheory)
								], debug=True)

