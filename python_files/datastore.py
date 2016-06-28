from google.appengine.ext import ndb

#--- datastore classes ----------

class Theory(ndb.Model):

	#login details
	email = ndb.StringProperty(required=True)
	password_hash = ndb.StringProperty(required=True)
	
	#user details	
	first_name = ndb.StringProperty(required=True)
	last_name = ndb.StringProperty(required=True)
	owner = ndb.StringProperty() #ID of user that owns this theory. Esto lo voy usar cuando permita log-in con una cuenta de Google
	
 	#user settings
 	language = ndb.StringProperty(choices=('Spanish', 'English'), default='English')
 	hide_private_ksus = ndb.BooleanProperty(default=False)
	
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


class Tag(ndb.Model):
	
	theory = ndb.KeyProperty(kind=Theory, required=True)
	created = ndb.DateTimeProperty(auto_now_add=True)		
	last_modified = ndb.DateTimeProperty(auto_now=True)
	
	name = ndb.StringProperty(required=True)
	description = ndb.StringProperty()
	ksus = ndb.KeyProperty(kind=Theory, repeated=True)	#all KSUs related to this tag


class KSU(ndb.Model):
	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	# base properties
	description = ndb.StringProperty(required=True)
	comments = ndb.TextProperty()
	ksu_type = ndb.StringProperty()
	ksu_subtype = ndb.StringProperty()

	value_type = ndb.StringProperty()
	local_category = ndb.StringProperty()
	tags = ndb.KeyProperty(kind=Tag, repeated=True) #all tags related to this KSU	
	parent_id = ndb.StringProperty()		
		
	is_active = ndb.BooleanProperty(default=True)
	is_critical = ndb.BooleanProperty(default=False)
	is_private = ndb.BooleanProperty(default=False)

	is_visible = ndb.BooleanProperty(default=True)
	is_deleted = ndb.BooleanProperty(default=False)

	# base properties - might be used in the future
	importance = ndb.IntegerProperty()
	picture = ndb.BlobProperty()
			
	# KAS Specific	
	last_event = ndb.DateProperty()
	next_event = ndb.DateProperty()
	pretty_next_event = ndb.StringProperty()
	
	best_time = ndb.TimeProperty()
	time_cost = ndb.IntegerProperty()

	repeats = ndb.StringProperty()	
	repeats_every = ndb.IntegerProperty()
	repeats_on = ndb.JsonProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year

	trigger_circumstances = ndb.TextProperty()
	standard_reward = ndb.IntegerProperty()
	valid_exceptions = ndb.TextProperty()	
	standard_punishment = ndb.IntegerProperty()

	# KAS Specific - might be used in the future
	Repetition_target_min = ndb.IntegerProperty()
	Repetition_target_max = ndb.IntegerProperty()
	TimeUse_target_min = ndb.IntegerProperty()
	TimeUse_target_max = ndb.IntegerProperty()

	#Objective Specific
	success_definition = ndb.StringProperty()
	target_date = ndb.DateProperty()
	pretty_target_date = ndb.StringProperty()
	is_BigO = ndb.BooleanProperty(default=False)

	#Wish Specific
	wish_categorie = ndb.StringProperty()
	money_cost = ndb.IntegerProperty()
	is_dream = ndb.BooleanProperty(default=False)

	#EVPo Specific
	charging_time = ndb.IntegerProperty()
	trigger_action = ndb.StringProperty()
	next_trigger_event = ndb.DateProperty()

	#Idea Specific
	source = ndb.StringProperty()
	is_principle = ndb.BooleanProperty(default=False)

	#Important person Specifics
	contact_frequency = ndb.IntegerProperty()
	contact_action = ndb.StringProperty()
	next_contact_event = ndb.DateProperty()
	impe_birthday = ndb.DateProperty()
	impe_kaswareID = ndb.StringProperty()

	#RTBG Specifics
	awesomeness = ndb.IntegerProperty()
	max_awesomeness = ndb.IntegerProperty() # To be used to track max awesomeness
	was_awesome = ndb.BooleanProperty(default=False)
	awesome_since = ndb.DateProperty()

	#Indicator Specifics
	question = ndb.StringProperty()
	question_time = ndb.StringProperty(default='morning')
	question_frequency = ndb.IntegerProperty()
	target_max = ndb.FloatProperty()
	target_min = ndb.FloatProperty()
	reverse_target = ndb.BooleanProperty(default=False)


class Event(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)
	ksu_id = ndb.KeyProperty(kind=KSU, required=True)	
	date = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	# base properties
	event_type = ndb.StringProperty(required=True)
	comments = ndb.TextProperty()

	#Score properties
	kpts_type = ndb.StringProperty()
	score = ndb.IntegerProperty(default=0)
	duration = ndb.IntegerProperty(default=0)
	intensity = ndb.IntegerProperty(default=0)



