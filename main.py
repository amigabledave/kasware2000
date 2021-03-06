#KASware V2.0.0 | Copyright 2016 Kasware Inc.
# -*- coding: utf-8 -*-
import webapp2, jinja2, os, re, random, string, hashlib, json, logging, math 

from datetime import datetime, timedelta, time, date
from google.appengine.ext import ndb
from google.appengine.api import mail
from python import datastore, randomUser, constants, kasware_os, KASware3

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

constants = constants.constants

Theory = datastore.Theory

KSU = datastore.KSU
KSU3 = datastore.KSU3

Event = datastore.Event
Event3 = datastore.Event3

os_ksus = kasware_os.os_ksus


template_dir = os.path.join(os.path.dirname(__file__), 'html')
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
		self.game = self.theory and self.update_game_log()

	def update_game_log(self):

		def check_and_burn(theory, active_date, time_travel):
			print
			print 'Esta a punto de hacer check and burn!'
			print

			game = theory.game 
			
			critical_burn = theory.game['critical_burn']
			mission_burn = theory.game['mission_burn']

			user_key = theory.key

			today =(datetime.today()+timedelta(hours=theory.timezone)+timedelta(days=time_travel)) 
			today_ordinal = active_date			
		
			ksu_set = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False, KSU.in_graveyard == False, KSU.is_active == True).fetch()
			# ksu_set = KSU.query(KSU.theory == user_key).filter(KSU.is_deleted == False, KSU.in_graveyard == False, KSU.is_active == True, KSU.is_critical == True)


			burn_candidates = []
			mission_burn_candidates = [] 

			burn_sets = ['KAS1', 'KAS2', 'EVPo', 'ImPe']
			mission_burn_sets = ['KAS1', 'KAS2', 'EVPo', 'ImPe', 'ImIn']

			for ksu in ksu_set:			
				if ksu.is_critical and ksu.ksu_subtype in burn_sets:
					burn_candidates.append(ksu)
				elif ksu.next_event and ksu.ksu_subtype in mission_burn_sets:
					mission_burn_candidates.append(ksu)


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

					# game['points_to_goal'] += kpts_burned
					game['points_today'] -= kpts_burned
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
			
			for ksu in mission_burn_candidates:

				next_event = ksu.next_event.toordinal()

				if next_event < today_ordinal:

					next_critical_burn = ksu.next_critical_burn
					if not ksu.next_critical_burn or next_critical_burn < next_event:
						next_critical_burn = next_event
					
					kpts_burned = (today_ordinal - next_critical_burn) * mission_burn

					# game['points_to_goal'] += kpts_burned
					game['points_today'] -= kpts_burned
					ksu.next_critical_burn = today_ordinal
					ksu.put()

					event = Event(
						theory=self.theory.key,
						ksu_id =  ksu.key,
						event_type = 'Stupidity',
						user_date_date=today,
						user_date=today_ordinal,
						score = kpts_burned,
						
						comments = 'Mission burn',
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
			# kpts_to_survive = (active_date - last_log - 1) * game['daily_goal'] + game['points_to_goal']
			kpts_to_survive = (active_date - last_log) * game['daily_goal']			
			game['piggy_bank'] += game['points_today']
			if kpts_to_survive <= game['piggy_bank']:
				game['streak'] += active_date - last_log
				game['piggy_bank'] -= kpts_to_survive
				if game['goal_achieved']:
					game['streak'] -= 1
			else:
				game['streak'] = 0
				game['piggy_bank'] = 0
			
			# game['points_to_goal'] = game['daily_goal']
			game['points_today'] = 0
			game['goal_achieved'] = False
			game['last_log'] = active_date
			theory.game = game
			theory.put()

		return game



# ---- KASware3 ----
class Home(Handler):

	@super_user_bouncer
	def get(self):
		constants['ksu_types'] = KASware3.ksu_types		
		new_pic_input_action = "{0}".format(blobstore.create_upload_url('/upload_pic'))
		self.print_html('KASware3.html', constants=constants, new_pic_input_action=new_pic_input_action)

	@super_user_bouncer
	def post(self):
		event_details = json.loads(self.request.body);
		user_action = event_details['user_action']	
		
		if user_action in ['Action_Done', 'Stupidity_Commited']:
			ksu = KSU3.get_by_id(int(event_details['ksu_id']))
			event = self.create_event(ksu, user_action, event_details)
			event.put()
			
			ksu = self.update_ksu(ksu, user_action)
			ksu.put()

			game = self.update_game(event)
			event_dic = self.event_to_dic(event)
			
			self.response.out.write(json.dumps({
				'mensaje': 'Evento guardado',
				'game':game,
				'event_dic':event_dic,
				'in_graveyard': ksu.in_graveyard,
				}))
			return

		elif user_action in ['Milestone_Reached', 'EndValue_Experienced', 'Measurement_Recorded']:
			ksu = KSU3.get_by_id(int(event_details['ksu_id']))
			
			event = self.create_event(ksu, user_action, event_details)
			event.put()
			
			ksu = self.update_ksu(ksu, user_action)
			ksu.put()

			event_dic = self.event_to_dic(event)
			
			self.response.out.write(json.dumps({
				'mensaje': 'Evento guardado',
				'event_dic':event_dic,
				'in_graveyard': ksu.in_graveyard,
				}))
			return

		elif user_action in ['Action_Skipped', 'Action_Pushed', 'SendToMission']: 
			ksu = KSU3.get_by_id(int(event_details['ksu_id']))
			ksu = self.update_event_date(ksu, user_action)
			ksu.put()

			new_event_date = ''
			if ksu.event_date:
				new_event_date = ksu.event_date.strftime('%Y-%m-%d')

			self.response.out.write(json.dumps({
				'mensaje':'Merit Event Created',
				'ksu_id': ksu.key.id(),
				'new_event_date': new_event_date,
				'description': ksu.description,
				}))
			return	

		elif user_action == 'RetrieveTheory':
			ksu_set = KSU3.query(KSU3.theory_id == self.theory.key).filter(KSU3.in_graveyard == False).fetch()
			ksu_output = []
			reasons_index = []
			
			for ksu in ksu_set:
				ksu_output.append(self.ksu_to_dic(ksu))
				reasons_index.append([ksu.key.id(), ksu.ksu_subtype, ksu.description])
			
			history = Event3.query(Event3.theory_id == self.theory.key).order(-Event3.event_date).fetch()
			event_output = []
			for event in history:
				event_output.append(self.event_to_dic(event))
				
			self.response.out.write(json.dumps({
				'mensaje':'Esta es la teoria del usuario:',
				'ksu_set': ksu_output,
				'history': event_output,
				'reasons_index':reasons_index,
				'ksu_type_attributes': KASware3.ksu_type_attributes,
				'attributes_guide': KASware3.attributes_guide,
				'reasons_guide': KASware3.reasons_guide,
				}))
			return

		elif user_action == 'SaveNewKSU':
			ksu = KSU3(theory_id=self.theory.key)
			ksu_type = event_details['ksu_type']
			attributes = self.get_ksu_type_attributes(ksu_type)

			for attribute in attributes:
				self.update_ksu_attribute(ksu, attribute, event_details[attribute])
				
			ksu.put()

			ksu_dic = self.ksu_to_dic(ksu)
			ksu_dic['mensaje'] = 'KSU3 creado y guardado desde el viewer!'
			self.response.out.write(json.dumps(ksu_dic))
			return

		elif user_action == 'DeleteKSU':
			ksu = KSU3.get_by_id(int(event_details['ksu_id']))

			child_ksus = KSU3.query(KSU3.reason_id == ksu.key).fetch()
			for child in child_ksus:
				child.reason_id = None
				child.put()

			ksu_events = Event3.query(Event3.ksu_id == ksu.key).fetch()
			for event in ksu_events:
				event.key.delete()

			ksu.key.delete()
			
			self.response.out.write(json.dumps({
				'mensaje':'KSU Borrado',
				'ksu_id': ksu.key.id(),
				'description': ksu.description,
				}))
			return

		elif user_action == 'DeleteEvent':
			event = Event3.get_by_id(int(event_details['event_id']))
			game = self.update_game(event, delete_event=True)
			ksu = KSU3.get_by_id(event.ksu_id.id())
			render_ksu = ksu.in_graveyard
			ksu.in_graveyard = False
			ksu.put()
			event.key.delete()
			
			self.response.out.write(json.dumps({
				'mensaje':'Evento Revertido',
				'ksu': self.ksu_to_dic(ksu),
				'game': game,
				'render_ksu': render_ksu,
				}))
			return

		elif user_action == 'UpdateKsuAttribute':

			ksu = KSU3.get_by_id(int(event_details['ksu_id']))
			self.update_ksu_attribute(ksu, event_details['attr_key'], event_details['attr_value'])

			event_dic = None
			if 'status' == event_details['attr_key']:
				status = event_details['attr_value']
				if status in ['Present', 'Past', 'Memory', 'Pursuit']:
					user_action = 'LifePieceTo_' + status
					event = self.create_event(ksu, user_action, {})
					event.put()	
					if user_action in ksu.details:
						Event3.get_by_id(int(ksu.details[user_action])).key.delete()
					ksu.details['LifePieceTo_' + status] = event.key.id()
					event_dic = self.event_to_dic(event)

			ksu.put()
			self.response.out.write(json.dumps({
				'mensaje':'Attributo actualizado',
				'event_dic': event_dic,
				'ksu_dic': self.ksu_to_dic(ksu)
				}))
			return
		
		elif user_action == 'RequestNewPicInputAction':
			new_pic_input_action = "{0}".format(blobstore.create_upload_url('/upload_pic'))
			self.response.out.write(json.dumps({
					'new_pic_input_action': new_pic_input_action,
					'mensaje':'Nueva accion enviada',
					}))
			return
		
		elif user_action == 'RetrieveDashboard':
			
			end_date = (datetime.strptime(event_details['period_end_date'], '%Y-%m-%d')) + timedelta(minutes=1439)
			start_date = end_date - timedelta(days=int(event_details['period_duration'])-1)
				
			dashboard_base = self.CreateDashboardBase(start_date, end_date)
			dashboard_sections = self.CreateDashboardSections(dashboard_base)

			self.response.out.write(json.dumps({
					'dashboard_sections': dashboard_sections,
					'mensaje':'Dashboard values calculated',
					}))
		return

	def update_ksu(self, ksu, user_action):

		if user_action == 'Action_Done':
			ksu = self.update_event_date(ksu, user_action)
			if ksu.details['repeats'] == 'Never' and ksu.ksu_subtype != 'Reactive':
				ksu.in_graveyard = True
		
		elif user_action == 'Milestone_Reached':
			ksu.in_graveyard = True

		elif user_action == 'EndValue_Experienced':
			if ksu.ksu_subtype in ['Moment', 'Chapter']:
				ksu.in_graveyard = True

		return ksu

	def update_ksu_attribute(self, ksu, attr_key, attr_value):

		attr_type = KASware3.attributes_guide[attr_key][0]
		fixed_key = attr_key
		fixed_value = attr_value
		event = None

		if attr_type in ['String', 'Text']:
			fixed_value = attr_value.encode('utf-8')
		
		elif attr_type == 'Integer':
			if attr_value != '':
				fixed_value = int(attr_value)
			else:
				fixed_value = 0
					
		elif attr_type == 'Details':
			fixed_key = 'details'
			details_dic = ksu.details
			details_dic[attr_key] = fixed_value
			fixed_value = details_dic
		
		elif attr_type == 'Key':
			fixed_value = None
			if attr_value != '':
				fixed_value = KSU3.get_by_id(int(attr_value)).key

		elif attr_type == 'DateTime':
			fixed_value = None
			if attr_value != '':
				fixed_value = datetime.strptime(attr_value, '%Y-%m-%d')		
	
		elif attr_type == 'BlobKey':
			fixed_value = None
			#Queda pendiente decirle que hacer con el blobkey

		setattr(ksu, fixed_key, fixed_value)
		return ksu, event
	
	def ksu_to_dic(self, ksu):
		ksu_dic = {
			'ksu_id': ksu.key.id(),
			'event_date': '',
			'reason_id': '',
		}
		
		ksu_attributes = self.get_ksu_type_attributes(ksu.ksu_type)
		details_dic = ksu.details

		for attribute in ksu_attributes:
			attr_type = KASware3.attributes_guide[attribute][0]

			if attr_type in  ['String', 'Text', 'Integer', 'Boolean']:
				ksu_dic[attribute] = getattr(ksu, attribute)
			
			elif attr_type == 'Details':
				if attribute in details_dic:
					ksu_dic[attribute] = details_dic[attribute]

		if ksu.event_date:
			ksu_dic['event_date'] = ksu.event_date.strftime('%Y-%m-%d'),
		
		if ksu.reason_id:
			ksu_dic['reason_id'] = ksu.reason_id.id()
						
		return ksu_dic

	def event_to_dic(self, event):
		event_dic = {
			'event_id': event.key.id(),
			'event_type': event.event_type,
			'score':event.score,
			'description': event.description,
			'event_date': event.event_date.strftime('%I:%M %p. %a, %b %d, %Y'),
			'counter': event.counter,
			'events':1
		}
		return event_dic

	def get_ksu_type_attributes(self, ksu_type):
		attributes = KASware3.ksu_type_attributes['Base'] + KASware3.ksu_type_attributes[ksu_type] 
		
		if ksu_type in ['Experience', 'Contribution', 'SelfAttribute', 'Person', 'Possesion', 'Environment']:
			attributes += KASware3.ksu_type_attributes['LifePiece']
		return attributes

	def update_event_date(self, ksu, user_action):
		today = (datetime.today()+timedelta(hours=self.theory.timezone))
		# today = datetime(2017,12,5)
		tomorrow = today + timedelta(days=1)
		ksu_details = ksu.details

		if user_action in ['Action_Done', 'Action_Skipped']:
			repeats = ksu_details['repeats']
			
			if repeats == 'Never':
				ksu.event_date = None
			
			elif repeats == 'Always':
				ksu.event_date = today

			elif repeats == 'X_Days':
				x_days = int(ksu.details['every_x_days'])
				ksu.event_date = today + timedelta(days=x_days)
				
			elif repeats == 'Week':
				todays_weekday = today.weekday()
				
				week = ['every_mon','every_tue','every_wed','every_thu','every_fri','every_sat', 'every_sun']
				week = week[todays_weekday:] + week[0:todays_weekday]
				week = week[1:7]

				x_days = 1
				for day in week:
					if ksu_details[day]:
						break
					else:
						x_days += 1				
				ksu.event_date = today + timedelta(days=x_days)

			elif repeats in ['Month', 'Year']:
				next_year = today.year
				
				if repeats == 'Month':					
					next_month = today.month + 1
					if next_month == 13:
						next_month = 1
						next_year += 1
				
				elif repeats == 'Year':
					next_month = int(ksu_details['of_month'])
					next_year += 1
				
				max_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
				next_day = min(int(ksu_details['on_the_day']), max_day[next_month - 1])
					
				ksu.event_date = datetime(next_year, next_month, next_day) 
				
		if user_action == 'Action_Pushed':
			ksu.event_date = tomorrow

		if user_action == 'SendToMission':
			ksu.event_date = today

		return ksu

	def create_event(self, ksu, user_action, event_details):
		weight = {1:1, 2:3, 3:5, 4:8, 5:13} #Peso para ponderar Life Pieces según su importancia/size
		ksu_subtype = ksu.ksu_subtype
		description = ksu.description

		if user_action == 'Action_Done':
			event_type = 'Effort'
		
		elif user_action == 'Stupidity_Commited':
			event_type = 'Stupidity'
			description = ksu.details['negative_alternative']

		elif user_action == 'Milestone_Reached':
			event_type = 'Progress'

		elif user_action == 'EndValue_Experienced':
			event_type = 'EndValue'

		elif user_action in ['LifePieceTo_Present','LifePieceTo_Memory']:
			event_type = 'WishRealized'

		elif user_action in ['LifePieceTo_Pursuit']:
			event_type = 'PursuitStarted'

		elif user_action == 'LifePieceTo_Past':
			event_type = 'LifePieceGone'

		elif user_action == 'Measurement_Recorded':
			description = ksu.details['question']
			if ksu_subtype == 'Perception':
				event_type = 'PerceptionSnapshot'
			elif ksu_subtype == 'Reality':
				event_type = 'RealitySnapshot'

		event_date = (datetime.today() + timedelta(hours=self.theory.timezone))
		if ksu.event_date and ksu_subtype not in ['Action', 'Objective']:
			event_date = ksu.event_date

		size = ksu.size
		if 'size' in event_details:
			size = int(event_details['size'])	

		score = 0
		if 'score' in event_details:
			score = int(event_details['score'])
			
		elif event_type in ['WishRealized', 'LifePieceGone']:
			score = weight[size]

		elif event_type == 'Progress':
			score = 1

		counter = 1
		if 'counter' in event_details:
			counter = int(event_details['counter'])
		
		reps = 1
		if 'reps' in event_details:
			reps = int(event_details['reps'])


		reason_status = 'NoReason'
		if ksu.reason_id:
			reason_ksu = KSU3.get_by_id(ksu.reason_id.id())
			reason_status = reason_ksu.status

		event = Event3(
			theory_id = ksu.theory_id,
			ksu_id = ksu.key,
			description = description,
			reason_status = reason_status,
			event_date = event_date, 

			event_type = event_type,
			score = score,
			counter = counter,

			size = size)

		return event

	def update_game(self, event, delete_event=False):
		theory = self.theory
		game = self.game
		event_type = event.event_type
		score = event.score
		if delete_event:
			score = -score

		if event_type == 'Effort':
			game['points_today'] += score
		
		elif event_type == 'Stupidity':
			game['points_today'] -= score 

		theory.game = game
		self.theory.put()
		return game

	def CreateDashboardBase(self, start_date, end_date):

		dashboard_base = {'current':{}, 'previous':{}}
			
		for time_frame in ['current', 'previous']:
			
			for ksu_type in KASware3.ksu_types:
				dashboard_base[time_frame][ksu_type[0][0]] = {}

				for event_type in KASware3.event_types:
					
					dashboard_base[time_frame][ksu_type[0][0]][event_type] = make_template('events_total')

			for event_type in KASware3.event_types:

				dashboard_base[time_frame][event_type] = make_template('events_total')

		period_len = end_date.toordinal() - start_date.toordinal() + 1
		previous_start_date = start_date - timedelta(days=period_len)
		history = Event3.query(Event3.theory_id == self.theory.key).filter(Event3.event_date >= previous_start_date, Event3.event_date <= end_date).order(-Event3.event_date).fetch()
	
		ksu_set = KSU3.query(KSU3.theory_id == self.theory.key).fetch()
		
		monitored_ksus = []
		monitored_ksus_ids = []
		monitored_ksus_dic = {}
		superficial_scores = {}
		
		for ksu in ksu_set:
			ksu_id = ksu.key.id()
			if ksu.ksu_type != 'Indicator':
				ksu_event_types = ['Effort', 'Stupidity']
			
			else:
				ksu_event_types = ['PerceptionSnapshot', 'RealitySnapshot']

			superficial_scores[ksu_id] = {'ksu_type': ksu.ksu_type}
			for ksu_event_type in ksu_event_types:				
				superficial_scores[ksu_id][ksu_event_type] = { 'current': make_template('events_total'), 'previous': make_template('events_total')}
			
			if ksu.monitor and not ksu.in_graveyard:
				monitored_ksus_ids.append(ksu_id)
				monitored_ksus_dic[ksu_id] = ksu	

		for event in history:

			event_type = event.event_type
			time_frame = 'current'
			event_date = event.event_date
			
			if event.event_date < start_date:
				time_frame = 'previous'

			ksu_id = event.ksu_id.id()
			ksu_type_summary = dashboard_base[time_frame][superficial_scores[ksu_id]['ksu_type']][event_type]
			event_type_summmary = dashboard_base[time_frame][event_type]
			if event_type in superficial_scores[ksu_id]:
				ksu_score_summary = superficial_scores[ksu_id][event_type][time_frame]

			event_dic = self.event_to_dic(event)

			for score_type in ['score', 'events', 'counter']:		
				ksu_type_summary[score_type] += event_dic[score_type]
				event_type_summmary[score_type] += event_dic[score_type]
				if event_type in superficial_scores[ksu_id]:
					ksu_score_summary[score_type] += event_dic[score_type]	

		for time_frame in ['current', 'previous']:			
			for event_type in KASware3.event_types:
				dashboard_base[time_frame][event_type] = self.add_average_to_events_total(dashboard_base[time_frame][event_type], period_len)

		deep_scores = self.calculate_deep_scores(ksu_set, superficial_scores, 4)

		monitored_ksus_sections = []
		for ksu_id in monitored_ksus_ids:
			ksu = monitored_ksus_dic[ksu_id]
			section = self.ksu_to_dashboard_section(ksu, deep_scores[ksu_id], period_len)
			monitored_ksus_sections.append(section)
			
			if ksu.ksu_subtype == 'Reactive':
				
				ksu.ksu_subtype = 'Negative'
				ksu.description = ksu.details['negative_alternative']
				section = self.ksu_to_dashboard_section(ksu, deep_scores[ksu_id], period_len)
				monitored_ksus_sections.append(section)

		dashboard_base['monitored_ksus_sections'] = monitored_ksus_sections

		return dashboard_base	

	def CreateDashboardSections(self, dashboard_base):

		game = self.game
		
		dashboard_sections = [
			{'section_type':'Overall',
			'section_subtype':'Overall',
			'sub_sections':[
				
				{'title': 'Endeavours',				
				'score': 'X', #game['endevours'],
				'contrast_title': 'Merits in current endevour:',
				'contrast': 'xx of xx'},

				{'title': 'Discipline Lvl.',
				'score': game['discipline_lvl'],
				'contrast_title': 'Days in current level:',
				'contrast': 'xx of xx'},

				{'title': 'Piggy Bank', #Formerly Merits Reserves
				'score': game['piggy_bank'],
				'contrast': game['best_piggy_bank']},
			]},
		
			{'section_type':'ActionsSummary',
			'section_subtype':'Summary',
			'title': 'Effort Made',
			'sub_sections':[
				{'title': 'Total',
				'operator': 'total',
				'score': dashboard_base['current']['Effort']['score'],
				'contrast':dashboard_base['previous']['Effort']['score']},

				{'title': 'Average',
				'operator': 'average',
				'score': dashboard_base['current']['Effort']['averages']['score'],
				'contrast':dashboard_base['previous']['Effort']['averages']['score']},
			]},

			{'section_type':'ActionsSummary',
			'section_subtype':'Summary',
			'title': 'Stupidity Commited',
			'sub_sections':[
				{'title': 'Total',
				'operator': 'total',
				'score': dashboard_base['current']['Stupidity']['score'],
				'contrast':dashboard_base['previous']['Stupidity']['score']},

				{'title': 'Average',
				'operator': 'average',
				'score': dashboard_base['current']['Stupidity']['averages']['score'],
				'contrast': dashboard_base['previous']['Stupidity']['averages']['score']},
			]},

			{'section_type':'ActionsSummary',
			'section_subtype':'Summary',
			'title': 'Milestones Reached',
			'sub_sections':[
				{'title': 'Total',
				'score': dashboard_base['current']['Progress']['score'],
				'contrast':dashboard_base['previous']['Progress']['score']},

				{'title': 'Average',
				'score': dashboard_base['current']['Progress']['averages']['score'],
				'contrast': dashboard_base['previous']['Progress']['averages']['score']},
			]},		


			{'section_type':'ActionsSummary',
			'section_subtype':'Summary',
			'title': 'Wishes Realized',
			'sub_sections':[
				{'title': 'Total',
				'score': dashboard_base['current']['WishRealized']['score'],
				'contrast':dashboard_base['previous']['WishRealized']['score']},

				{'title': 'Average',
				'score': dashboard_base['current']['WishRealized']['averages']['score'],
				'contrast': dashboard_base['previous']['WishRealized']['averages']['score']},
			]},


		]


		section_titles = {
			'Progress': 'Milestones Reached',
			'WishRealized': 'Wishes Realized'
		}
		

		for event_type in ['WishRealized']:
			section = {
				'section_type':'LifePiecesSummary',
				'section_subtype':'Summary',
				'title': section_titles[event_type],
				'sub_sections':[]
			}

			for ksu_type in KASware3.life_pieces:
				section['sub_sections'].append({
					'glyphicon': ksu_type[1],
					'score': dashboard_base['current'][ksu_type[0]][event_type]['score'],
					'contrast': dashboard_base['previous'][ksu_type[0]][event_type]['score']
				})

			dashboard_sections.append(section)

		return dashboard_sections + dashboard_base['monitored_ksus_sections']

	def add_average_to_events_total(self, events_total, period_len):
		events_total['averages'] = {}
		for section in ['score', 'events', 'counter']:
			events_total['averages'][section] = round(events_total[section]/(period_len*1.0),1)

		return events_total

	def ksu_to_dashboard_section(self, ksu, ksu_deep_score, period_len):#xx
		
		event_type = 'Effort'		
		
		goal_factor = (period_len * 1.0 /int(ksu.details['goal_time_frame']))
		for goal in ['goal_score', 'goal_counter', 'goal_events']:
			if ksu.details[goal] == '':
				ksu.details[goal] = 0
			elif ksu.ksu_type != 'Indicator':
				ksu.details[goal] = round(int(ksu.details[goal]) * goal_factor, 1)
			else:
				ksu.details[goal] = float(ksu.details[goal])

		ksu_subtype = ksu.ksu_subtype
		sub_sections_titles = {'score':'Merits Earned', 'events':'Total Actions', 'counter':'Total Minutes'}
		
		if ksu_subtype == 'Reactive':
			sub_sections_titles['counter'] = 'Total Repetitions'
		
		elif ksu_subtype == 'Negative':
			event_type = 'Stupidity'
			sub_sections_titles['counter'] = 'Total Repetitions'
			sub_sections_titles['score'] = 'Merits Loss'

		print
		print ksu_deep_score
		print

		section = {
			'section_type':'KsuSummary',	
			'title':ksu.description,
			'ksu_type': ksu.ksu_type,
			'section_subtype': 'MonitoredKSU',			
			'sub_sections':[]}


		if ksu.ksu_subtype in ['Reactive', 'Negative']:
			section['sub_sections'] = [
				{'title':sub_sections_titles['score'],
				'score':ksu_deep_score[event_type]['current']['score'],				
				'contrast_title': 'PP: ',
				'contrast':ksu_deep_score[event_type]['previous']['score']},

				{'title': sub_sections_titles['counter'],
				'score':ksu_deep_score[event_type]['current']['counter'],
				'contrast_title': 'PP: ',
				'contrast':ksu_deep_score[event_type]['previous']['counter']},

				{'title':sub_sections_titles['events'],
				'score':ksu_deep_score[event_type]['current']['events'],
				'contrast_title': 'PP: ',
				'contrast':ksu_deep_score[event_type]['previous']['counter']}
			]


		elif ksu.ksu_type != 'Indicator':
			section['sub_sections'] = [
				{'title':sub_sections_titles['score'],
				'score':ksu_deep_score[event_type]['current']['score'],				
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_score']},

				{'title': sub_sections_titles['counter'],
				'score':ksu_deep_score[event_type]['current']['counter'],
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_counter']},

				{'title':sub_sections_titles['events'],
				'score':ksu_deep_score[event_type]['current']['events'],
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_events']}
			]

		elif ksu_subtype == 'Reality':
			sub_sections_titles['events'] = 'Data Points'
			event_type = 'RealitySnapshot'
			section['sub_sections'] = [				
				{'title':'Period Average',
				'score':1.0*ksu_deep_score[event_type]['current']['score']/ksu_deep_score[event_type]['current']['events'],				
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_score']},

				{'title':sub_sections_titles['events'],
				'score':ksu_deep_score[event_type]['current']['events'],
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_events']}
			]

		elif ksu_subtype == 'Perception':
			sub_sections_titles['events'] = 'Data Points'
			event_type = 'PerceptionSnapshot'
			section['sub_sections'] = [				
				{'title':'Period Average',
				'score':str(int(100.0*ksu_deep_score[event_type]['current']['score']/ksu_deep_score[event_type]['current']['events']))+'%',				
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_score']},

				{'title':sub_sections_titles['events'],
				'score':ksu_deep_score[event_type]['current']['events'],
				'contrast_title': 'Goal',
				'contrast':ksu.details['goal_events']}
			]

		return section		

	def calculate_deep_scores(self, ksu_set, superficial_scores, generations):

		parent_ksus = []
		parent_childs = {}
		deep_scores = superficial_scores.copy()

		for ksu in ksu_set:
			
			ksu_id = ksu.key.id()
			reason_id = ksu.reason_id
			
			if reason_id:
				reason_id = reason_id.id()
				if reason_id not in parent_ksus:
					parent_ksus.append(reason_id)
					parent_childs[reason_id] = [ksu_id]
				
				elif ksu_id not in parent_childs[reason_id]:
					parent_childs[reason_id].append(ksu_id)

		for i in range(generations):
			for ksu in parent_ksus:
				new_childs = [] + parent_childs[ksu]
				for child in parent_childs[ksu]:
					if child in parent_childs:
						for grand_child in parent_childs[child]: 
							if grand_child not in new_childs:
								new_childs.append(grand_child)
				parent_childs[ksu] = new_childs

		
		for time_frame in ['current', 'previous']:
			
			for ksu in parent_ksus:
				parent_deep_score = deep_scores[ksu]
				score_types = ['score', 'events', 'counter']

				for child in parent_childs[ksu]:
					child_superficial_score = superficial_scores[child]
					for event_type in ['Effort', 'Stupidity']:

						if event_type in parent_deep_score and event_type in child_superficial_score:

							for score_type in score_types:
								parent_deep_score[event_type][time_frame][score_type] += child_superficial_score[event_type][time_frame][score_type]

		return deep_scores


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
			post_details.update(randomUser.createRandomUser()) ## Creates a random user for testing Contributions
		
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
		logging.info('These are the post details: ') #Asi es como se imprime algo en la consola de windows
		logging.info(post_details)

		if user_action == 'SaveChanges':
			theory = self.theory
			game = self.game

			theory.first_name = post_details['first_name'].encode('utf-8') 
			theory.last_name = post_details['last_name'].encode('utf-8')	
	 	
	 		theory.language = str(post_details['language'])
	 		
	 		if 'hide_private_ksus' in post_details:
	 			theory.hide_private_ksus = True
			else:
				theory.hide_private_ksus = False

		 	theory.timezone = int(post_details['timezone'])
 			
			game['mission_burn'] = int(post_details['mission_burn'])
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

	
class PicuteUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	# @super_civilian_bouncer
	def post(self):		
		
		ksu_id = self.request.get('ksu_id')
		
		# logging.info('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		# logging.info('Event details')
		# logging.info(event_details)
		# logging.info('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')	

		ksu = KSU3.get_by_id(int(ksu_id))
		upload = self.get_uploads()[0]
		
		ksu.pic_key = upload.key();
		ksu.pic_url = images.get_serving_url(blob_key=upload.key())
		ksu.put()

		self.response.out.write(json.dumps({
				'message':'imagen guardada!!!'
			}))	
		

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
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False).order(-KSU.importance).order(KSU.created).fetch()
		
		elif set_name == 'TheoryQuery':
			lookup_string = self.request.get('lookup_string')
			user_theory = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.is_deleted == False).order(-KSU.importance).fetch() 
			# user_theory = KSU.query(KSU.theory == user_key ).order(KSU.importance).order(KSU.created).fetch() #TBD
			ksu_set = self.search_theory(user_theory, lookup_string)
			set_title = 'You searched for: ' + lookup_string
		
		elif set_name == 'Graveyard':
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == True, KSU.is_deleted == False).order(-KSU.importance).fetch()

		elif ksu_id:			
			ksu = KSU.get_by_id(int(ksu_id))
			ksu_key = ksu.key			
			ksu_set = KSU.query(KSU.parent_id == ksu_key).filter(KSU.is_deleted == False).order(-KSU.importance).fetch()
			set_title = ksu.description
			parent_id = int(ksu_id)
			dreams = self.get_active_dreams(user_key)
			objectives = self.get_user_objectives(user_key)
			# if set_name == 'BOKA':				
				# objectives, big_objectives = self.get_user_objectives(user_key)
				# objectives = self.get_user_objectives(user_key)
			view_type ='Plan'
		
		else:
			ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False, KSU.ksu_type == set_name).order(-KSU.importance)

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
			ksu['ksu_type'] = 'KAS2'
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
			ksu_set = ksu_set.order(-KSU.importance).fetch()
		else:
			ksu_set = ksu_set.order(-KSU.importance).fetch()

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
			
			elif ksu_subtype == 'BigO':
				objectives.append((ksu.key.id(), ksu.description))

			elif ksu_subtype == 'Wish' and ksu.is_critical:
				dreams.append((ksu.key.id(), ksu.description))
			

		return full_mission, objectives, today , dreams 


class TheoryViewer(Handler):

	@super_user_bouncer
	def get(self):
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False).order(-KSU.importance).fetch()

		for ksu in ksu_set:
			ksu.description_rows = determine_rows(ksu.description)
			ksu.secondary_description_rows = determine_rows(ksu.secondary_description)
			ksu.comments_rows = determine_rows(ksu.comments)

		tags = self.theory.categories['tags'] # por el quick adder

		self.print_html(
				'TheoryViewer.html',
				viewer_mode='Set', 
				ksu_set=ksu_set,
				set_name='KeyA', 
				constants=constants, 			
				ksu={}, 
				tags=tags)


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
				'kpts_value':ksu.kpts_value,
				'importance': ksu.importance
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
				game['points_today'] += score

			elif kpts_type in ['SmartEffort', 'EndValue']:
				# game['points_to_goal'] += score
				game['points_today'] -= score			
			
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
				# 'PointsToGoal': game['points_to_goal'],
				'PointsToday': game['points_today'],
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
			if attr_key == 'effort_denominator' and ksu.ksu_subtype == 'EVPo':
				self.update_single_attribute(ksu, 'kpts_value', attr_value)
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
				
				if ksu_subtype == 'EVPo' or ksu.is_jg:
					event.kpts_type = 'EndValue'

				if ksu_subtype == 'KAS2':
					if ksu.is_mini_o:
						# print 'Si se dio cuenta de que es un MiniO'
						ksu.secondary_description = None
						ksu.best_time = None
						ksu.kpts_value = 1
					else:
						ksu.is_deleted = True

				update_next_event(self, user_action, {}, ksu)

				# if ksu_subtype in ['EVPo']:
				# 	event.quality = event_details['event_quality']

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
											
											'PointsToday': game['points_today'],
											# 'PointsToGoal':game['points_to_goal'],
											'EffortReserve':game['piggy_bank'],
											'Streak':game['streak']}))
		return


	def update_active_log(self, event):

		game = self.game

		minimum_daily_effort = game['daily_goal']

		# if event.kpts_type == 'SmartEffort':
		# 	if  game['points_to_goal'] == 0:
		# 		game['piggy_bank'] += event.score
			
		# 	elif event.score >= game['points_to_goal']:
		# 		game['piggy_bank'] += event.score - game['points_to_goal'] 
 	# 			game['points_to_goal'] = 0
 	# 			if not game['goal_achieved']:
	 # 				game['goal_achieved'] = True
	 # 				game['streak'] += 1

 	# 		else: 				 
 	# 			game['points_to_goal'] -= event.score

		# if event.kpts_type == 'Stupidity':
		# 	game['points_to_goal'] += event.score
		
		if event.kpts_type in ['SmartEffort', 'EndValue']:
			game['points_today'] += event.score

		elif event.kpts_type == 'Stupidity':
			game['points_today'] -= event.score

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

		elif attr_key in ['is_critical', 'is_private', 'is_active', 'is_mini_o', 'is_jg']:
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


		elif attr_key in ['positive_label', 'negative_label', 'neutral_label', 'units']:
			print
			print 'So far si esta intentando actualizar el label del indicador'
			print
			ksu.ImIn_details[attr_key] = attr_value.encode('utf-8')


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
		self.redirect('/')

	def populateRandomTheory(self):

		post_details = {'user_action':'Random_SignUp'}
		user_action = 'Random_SignUp'

		if user_action == 'Random_SignUp':
			post_details.update(randomUser.createRandomUser()) ## Creates a random user for testing Contributions
		
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
			[0, {'ksu_type':'BigO', 'ksu_subtype':'BigO'}],
			[0, {'ksu_type':'Wish', 'ksu_subtype':'Wish'}],
			[0, {'ksu_type':'EVPo', 'ksu_subtype':'EVPo', 'next_event':today, 'kpts_value':1, 'frequency':7}],
			[0, {'ksu_type':'ImPe', 'ksu_subtype':'ImPe', 'next_event':today, 'kpts_value':0.25, 'frequency':30}],
			[0, {'ksu_type':'Idea', 'ksu_subtype':'Idea'}],
			[0, {'ksu_type':'RTBG', 'ksu_subtype':'RTBG'}],
			[0, {'ksu_type':'Diary', 'ksu_subtype':'Diary', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'RealitySnapshot', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'BinaryPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'TernaryPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],			
			[0, {'ksu_type':'ImIn', 'ksu_subtype':'FibonacciPerception', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'frequency':1}],			
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS3'}],
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS4'}],
			[0, {'ksu_type':'KeyA', 'ksu_subtype':'KAS1', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':2, 'frequency':1, 'repeats':'R001'}],
			[0, {'ksu_type':'OTOA', 'ksu_subtype':'KAS2', 'next_event':today, 'pretty_next_event':today.strftime('%a, %b %d, %Y'), 'kpts_value':3}],

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

				new_ksu.importance = (theory.size + 1) * 10000 
				theory.size += 1
				theory.put() 	

				new_ksu.put()		
		return


class UpdateTheoryStructure(Handler):
	
	@super_user_bouncer
	def get(self):
		user_key = self.theory.key
		ksu_set = KSU.query(KSU.theory == user_key ).filter(KSU.in_graveyard == False).order(-KSU.importance).fetch()	
		
		self.recalibrate_theory_importance(ksu_set, self.theory.size)
		self.redirect('/MissionViewer?time_frame=Today')


	def recalibrate_theory_importance(self, ordered_ksu_set, theory_size):		
		theory = self.theory
		theory_size = 0
		next_importance = 10000 
		for ksu in ordered_ksu_set:
			ksu.importance = next_importance
			next_importance += 10000
			ksu.put()
			theory_size += 1
		theory.size = theory_size
		theory.put()


class PopulateRandomHistory(Handler):
	
	@super_user_bouncer
	def get(self):
		
		valid_subtypes = ['Proactive', 'Rective', 'Negative']
		n = 2

		ksu_set = KSU3.query(KSU3.theory_id == self.theory.key).fetch()
		for ksu in ksu_set:
			if ksu.ksu_subtype in valid_subtypes:
				for i in range(0, n):
					self.create_random_event(ksu)

		self.redirect('/')

	def create_random_event(self, ksu):
		event_date = datetime.today() - timedelta(days=random.randrange(0,13))
		ksu_event_by_subtype = {
			'Proactive':'Effort',
			'Reactive': 'Effort',
			'Negative':'Stupidity'
		}

		event = Event3(
			theory_id = ksu.theory_id,
			ksu_id = ksu.key,
			description = ksu.description,
			event_date = event_date, 

			event_type = ksu_event_by_subtype[ksu.ksu_subtype],
			score = random.randrange(0, 40),
			counter = random.randrange(0, 120),
			size = random.randrange(1, 5),
			comments = '')
		event.put()



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

	today = (datetime.today()+timedelta(hours=self.theory.timezone))
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

	if ksu.ksu_subtype == 'EVPo' or ksu.is_jg:
		ksu.kpts_value = ksu.effort_denominator

	print
	print 'Este es el nuevo sub tipo de KSU que estoy creando'
	print ksu.ksu_type
	print ksu.ksu_subtype

	ksu.importance = (theory.size + 1) * 10000 
	theory.size += 1
	theory.put() 

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


#KASWare3	
def make_template(template_name):
	templates = {
		'event_type_summary': {'score':{1:0, 2:0, 3:0, 4:0, 5:0, 'total':0}, 'events':{1:0, 2:0, 3:0, 4:0, 5:0, 'total':0}, 'days':[]},
		'merits_summary': {'score':{'total':0, 'average':0}, 'events':{'total':0, 'average':0}},
		'events_total': {'score':0, 'events':0, 'counter':0}
	}
	return templates[template_name]

def calculate_mission_reward(eod_merits, merits_goal):
	
	bracket_size = 20
	reward_factor = 1
	reward = 0

	range_end = eod_merits - merits_goal

	if range_end < 0:
		reward_factor = -1
		range_end = -range_end

	for merit in range(0, range_end):
		merit_reward = math.floor(merit/bracket_size) + 1
		reward += merit_reward

	return reward * reward_factor


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


#--- Theory Structure Updates
class UpdateTheories(Handler):
	def get(self):
		theories = Theory.query().fetch()
		self.update_all_theories(theories)
		self.redirect('/Settings')
		return

	def update_all_theories(self, theories):
		for theory in theories:
			theory['something'] = 0
		return		


#--- Request index
app = webapp2.WSGIApplication([
	('/', Home),
	('/KASware3', Home),
	('/upload_pic', PicuteUploadHandler),

	('/SignUpLogIn', SignUpLogIn),
	('/Accounts', Accounts),
	('/LogOut', LogOut),
	('/Settings', Settings),

	('/KsuEditor', KsuEditor),
	('/MissionViewer', MissionViewer),
	('/SetViewer', SetViewer),
	('/TheoryViewer', TheoryViewer),

	('/EventHandler',EventHandler),
	('/HistoryViewer', HistoryViewer),

	('/PopulateRandomTheory',PopulateRandomTheory),
	('/PopulateRandomHistory', PopulateRandomHistory),
	('/UpdateTheoryStructure', UpdateTheoryStructure),
	# ('/UpdateTheories', UpdateTheories)
], debug=True)

