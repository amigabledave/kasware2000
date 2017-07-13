from google.appengine.ext import ndb

#Dejar claros todos los nuevos tipos y subtypos de KSUs
#Crear una nueva estructura de KSU en datastore

#Programar el nuevo template universal
#Code it in a way it supports something...


ksu_types = {
	

	# Result 
	'Experience':[
		'EndValue',
		'Growth'
	],
	
	'Indicator': [
		'RealitySnapshot',
		'BinaryPerception',
	]


	#Life Pieces
	'Meaning':[
		'GreaterGood', #Impact the life of others
		'SelfFocus' #Proof something mainly to your self. Achievement.
	],

	'Being':[
		'KnowledgeOrSkill', #'Mind', #Knowledge and skills
		'Attitude', #'Soul', #Connciousness and inner peace
		'PhisicalAttribute', #'Body', #Health and vitality
		'JoyGenerator'	
	],
	
	'Environment':[#'Stuff', #Environment & Stuff. Stuff & Other order and peace
		'Stuff',
		'Surroundings'
	],

	'Person':[ #'Love', #Important People. Love & Friendship
		'Friend',
		'Partner',
		'Child',
		'Family',
		'Pet',
		'Network',
	],
					
	'Power':[ #Money & Power
		'Money',
		'Status'
	], 		

	
	#Actions
	
	'Wisdom':[] #Your personal constitution #If the idea has a parent then is not a principle. BRILIANT!

	'Objective': [],

	'Action': [
		'Proactive',
		'Reactive',
		'Negative'
	],
	
}

class KSU3(ndb.Model):
	theory = ndb.KeyProperty(kind=Theory, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)
	ksu_type = ndb.StringProperty()
	ksu_subtype = ndb.StringProperty()
	parent_id = ndb.KeyProperty()

	description = ndb.StringProperty(required=True)	
	pic_key = ndb.BlobKeyProperty() #
	
	size = ndb.IntegerProperty(default=3) #Indicates the size of a LifePiece or Objective. In a fibonacci scale 1, 2, 3, 5, 8. Also works as effor denominator for Actions
	timer = ndb.IntegerProperty(default=0) #Total minutes invested
	event_date = ndb.DateProperty()

	is_realized = ndb.BooleanProperty(default=False) #Indicates if a 'LifePiece' is either a wish or a RTBG. And if an objective is acomplished or not.
	is_active = ndb.BooleanProperty(default=False) #Indicates if a 'LifePiece' is still part of my life situation
	is_critical = ndb.BooleanProperty(default=False)
	is_any_any = ndb.BooleanProperty(default=False)	

	is_visible = ndb.BooleanProperty(default=True)
	is_private = ndb.BooleanProperty(default=False)
	in_graveyard = ndb.BooleanProperty(default=False)

	comments = ndb.TextProperty()
	details = ndb.JsonProperty() # Subtype details. E.g. Birthday for a person, or exceptions for KAS4, Triggers for KAS3, cost for stuff	
	# best_time = ndb.TimeProperty()
	# frequency = ndb.JsonProperty() #Now this will include the repeats and repeats_on attributes
	# target = ndb.JsonProperty()
	# cost = ndb.JsonProperty(default={'money_cost':0, 'days_cost':0, 'hours_cost':0})
	# ImIn_details = ndb.JsonProperty(default={'positive_label':'Delighted', 'neutral_label':'Satisfied', 'negative_label':'Dissapointed', 'units':'Units'})	




#--- OLD datastore classes ----------

class Theory(ndb.Model):

	#login details
	email = ndb.StringProperty(required=True)
	valid_email = ndb.BooleanProperty(default=False)
	password_hash = ndb.StringProperty(required=True)

	#user details	
	first_name = ndb.StringProperty(required=True)
	last_name = ndb.StringProperty(required=True)
	owner = ndb.StringProperty() #ID of user that owns this theory. Esto lo voy usar cuando permita log-in con una cuenta de Google
	
 	#user settings
 	language = ndb.StringProperty(choices=('Spanish', 'English'), default='English')
 	hide_private_ksus = ndb.BooleanProperty(default=False)
 	timezone = ndb.IntegerProperty(default=-6) #Deberia de ser forzoza, pero para evitar errores por ahora no la solicito asi
 	# day_start_time = ndb.TimeProperty() - TBD
 	categories = ndb.JsonProperty(required=True)
 	size = ndb.IntegerProperty(default=0)

 	#Game details
 	game = ndb.JsonProperty(default={
 		'daily_goal':100,
 		'critical_burn':10,
 		'mission_burn':5,
 		'piggy_bank':0, 
 		'streak':0,
 		'last_log':None,
 		'goal_achieved':False,
 		'points_today':0,
 		'points_to_goal':100}) 
	
	#tracker fields
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	@classmethod # This means you can call a method directly on the Class (no on a Class Instance)
	def get_by_theory_id(cls, theory_id):
		return Theory.get_by_id(theory_id)

	@classmethod
	def get_by_email(cls, email):
		return Theory.query(Theory.email == email).get()

	@classmethod
	def valid_login(cls, email, password):
		theory = cls.get_by_email(email)
		if theory and validate_password(email, password, theory.password_hash):
			return theory


class KSU(ndb.Model):

	theory = ndb.KeyProperty(kind=Theory, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	description = ndb.StringProperty(required=True)
	secondary_description = ndb.StringProperty()

	comments = ndb.TextProperty()
	ksu_type = ndb.StringProperty()
	ksu_subtype = ndb.StringProperty()
	kpts_value = ndb.FloatProperty()

	importance = ndb.IntegerProperty(default=3)
	tags = ndb.StringProperty()
	parent_id = ndb.KeyProperty() # Ahora me esta dando un error porque lo estoy ligando a la misma clase que estoy definiendo
		
	is_active = ndb.BooleanProperty(default=True)
	is_critical = ndb.BooleanProperty(default=False)
	is_private = ndb.BooleanProperty(default=False)

	is_visible = ndb.BooleanProperty(default=True)
	in_graveyard = ndb.BooleanProperty(default=False)
	is_deleted = ndb.BooleanProperty(default=False)			

	next_event = ndb.DateProperty()
	pretty_next_event = ndb.StringProperty()
	frequency = ndb.IntegerProperty(default=1)
	repeats = ndb.StringProperty() # KAS1 Specific		
	repeats_on = ndb.JsonProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year
	
	mission_view = ndb.StringProperty(default='Principal')
	best_time = ndb.TimeProperty()
	pretty_best_time = ndb.StringProperty()

	is_mini_o = ndb.BooleanProperty(default=False)
	is_jg = ndb.BooleanProperty(default=False)
	target = ndb.JsonProperty() # For ksus that generate kpts and indicators target min, target max, reverse target etc
	birthday = ndb.DateProperty()
	
	timer = ndb.JsonProperty(default={'hours':0, 'minutes':0, 'seconds':0, 'value':'00:00:00'})
	cost = ndb.JsonProperty(default={'money_cost':0, 'days_cost':0, 'hours_cost':0})

	picture = ndb.BlobProperty() #Might be used in the future
	times_reviewed = ndb.IntegerProperty(default=0)
	next_critical_burn = ndb.IntegerProperty() #Define siguiente fecha como ordinal en la que si no se cumplio la accion esta quema

	effort_denominator = ndb.IntegerProperty(default=3)
	wish_type = ndb.StringProperty(default='doing')
	ImIn_details = ndb.JsonProperty(default={'positive_label':'Delighted', 'neutral_label':'Satisfied', 'negative_label':'Dissapointed', 'units':'Units'})
	

class Event(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)
	ksu_id = ndb.KeyProperty(kind=KSU, required=True)
	parent_id = ndb.KeyProperty(kind=KSU)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	is_deleted = ndb.BooleanProperty(default=False)

	# base properties
	user_date_date = ndb.DateTimeProperty(required=True)	
	user_date = ndb.IntegerProperty(required=True)
	event_type = ndb.StringProperty(required=True)
	
	comments = ndb.TextProperty()
	secondary_comments = ndb.StringProperty() #Para ponerle titulos a los eventos cuando aplique
	is_private = ndb.BooleanProperty(default=False)
	importance = ndb.IntegerProperty(default=3) #No me acuerdo para que era la importancia en el evento. Puede volver a servir despues como denominador

	#Score properties
	kpts_type = ndb.StringProperty()
	score = ndb.FloatProperty(default=0)
	quality = ndb.StringProperty()

	#KSU properties
	ksu_description = ndb.StringProperty()
	ksu_secondary_description = ndb.StringProperty()	
	ksu_subtype = ndb.StringProperty()
	ksu_tags = ndb.StringProperty()
