from google.appengine.ext import db


#--- datastore classes ----------

class Theory(db.Model):

	#login details		
	email = db.EmailProperty(required=True)
	password_hash = db.StringProperty(required=True)
	
	#user details	
	first_name = db.StringProperty(required=True)
	last_name = db.StringProperty(required=True)
	owner = db.StringProperty() #ID of user that owns this theory. Esto lo voy usar cuando permita log-in con una cuenta de Google
	
 	#user settings
 	language = db.StringProperty(choices=('Spanish', 'English'), default='English')
 	hide_private_ksus = db.BooleanProperty(default=False)
	
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)

	@classmethod # This means you can call a method directly on the Class (no on a Class Instance)
	def get_by_theory_id(cls, theory_id):
		return Theory.get_by_id(theory_id)

	@classmethod
	def get_by_email(cls, email):
		return Theory.all().filter('email =', email).get()

	@classmethod
	def valid_login(cls, email, password):
		theory = cls.get_by_email(email)
		if theory and validate_password(email, password, theory.password_hash):
			return theory





class GlobalTag(db.Model):
	
	theory = db.ReferenceProperty(Theory, collection_name='GlobalTags')
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)
	
	name = db.StringProperty(required=True)
	description = db.StringProperty()

	ksus = db.ListProperty(db.Key) 	#all KSUs related to this tag



class KAS1(db.Model):

	theory = db.ReferenceProperty(Theory, collection_name='KAS1')	
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)

	# base KSU properties
	description = db.StringProperty(required=True)
	status = db.StringProperty(choices=('Active', 'Done', 'Hold', 'Deleted'))
	
	ksu_id = db.StringProperty(required=True)
	ksu_type = db.StringProperty(required=True)
	ksu_subtype = db.StringProperty()
	parent_id = db.StringProperty()	
			
	is_visible = db.BooleanProperty(default=True)
	is_private = db.BooleanProperty(default=False)

	global_tags = db.ListProperty(db.Key) #all global tags related to this KSU
	local_tags = db.ListProperty(db.Key) #all local tags related to this KSU	
	origin = db.TextProperty() #Quien lo recomendo o como fue que este KSU llego a mi teoria
	comments = db.TextProperty()
	picture = db.BlobProperty()

	#KAS KSU propeties
	value_type = db.StringProperty(required=True, choices=('V000', 'V100', 'V200', 'V300', 'V400', 'V500', 'V600', 'V700', 'V800', 'V900'))
	importance = db.IntegerProperty(choices=(1,2,3,5,8), default=3)
	is_critical = db.BooleanProperty(default=False)

	#proactive KAS KSU	
	in_mission = db.BooleanProperty(default=False)
	any_any = db.BooleanProperty(default=False)
	in_upcoming = db.BooleanProperty(default=True)
	

	#date, time and frequency details
	next_event = db.DateProperty(required=True)
	best_time = db.TimeProperty()
	time_cost = db.IntegerProperty(default=1)
	repeats = db.StringProperty(required=True, choices=('Daily', 'Weekly', 'Monthly', 'Yearly'))	
	repeats_every = db.IntegerProperty(required=True)
	repeats_on = db.StringListProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year
	

	# KAS1 specifics
	last_event = db.DateProperty()
	project = db.StringProperty()

	TimeUse_target_min = db.IntegerProperty()
	TimeUse_target_max = db.IntegerProperty()
	Repetition_target_min = db.IntegerProperty()
	Repetition_target_max = db.IntegerProperty()



class KAS1LocalTag(db.Model):

	theory = db.ReferenceProperty(Theory, collection_name='KAS1LocalTags')
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)
	
	name = db.StringProperty(required=True)
	description = db.StringProperty()

	ksus = db.ListProperty(db.Key) 	#all KSUs related to this tag



