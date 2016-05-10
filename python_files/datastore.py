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
	#tracker fields
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	
	name = ndb.StringProperty(required=True)
	description = ndb.StringProperty()

	ksus = ndb.KeyProperty(kind=Theory, repeated=True)	#all KSUs related to this tag



class KSU(ndb.Model):
	#tracker fields
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	# base KSU properties
	description = ndb.StringProperty(required=True)
	status = ndb.StringProperty(choices=('Active', 'Done', 'Hold', 'Deleted'))

	# theory = ndb.ReferenceProperty(Theory, collection_name='KSUs')	#Included on last level
	# ksu_type = ndb.StringProperty(required=True) #Included on last level
	# ksu_id = ndb.StringProperty(required=True) #Not sure if with the new datastore structure is really necesary

	ksu_subtype = ndb.StringProperty()
	parent_id = ndb.StringProperty()	
			
	is_visible = ndb.BooleanProperty(default=True)
	is_private = ndb.BooleanProperty(default=False)

	tags = ndb.KeyProperty(kind=Tag, repeated=True) #all tags related to this KSU	
	comments = ndb.TextProperty()
	picture = ndb.BlobProperty()

	value_type = ndb.StringProperty(required=True, choices=('V00','V09', 'V10', 'V20', 'V30', 'V40', 'V50', 'V60', 'V70', 'V80', 'V90'), default='V09')
	importance = ndb.IntegerProperty(default=3)
	is_critical = ndb.BooleanProperty(default=False)



class KAS(KSU):
			
	in_mission = ndb.BooleanProperty(default=False)
	any_any = ndb.BooleanProperty(default=False)
	in_upcoming = ndb.BooleanProperty(default=True)

	next_event = ndb.DateProperty()
	best_time = ndb.TimeProperty()
	time_cost = ndb.IntegerProperty(default=1)

	Repetition_target_min = ndb.IntegerProperty()
	Repetition_target_max = ndb.IntegerProperty()

	project = ndb.StringProperty()



class KAS1(KAS):
		
	theory = ndb.KeyProperty(kind=Theory, required=True)
	ksu_type = ndb.StringProperty(default='KAS1') 
	
	last_event = ndb.DateProperty()
	repeats = ndb.StringProperty(required=True, choices=('R001', 'R007', 'R030', 'R365'), default='R001')	
	repeats_every = ndb.IntegerProperty(required=True, default=1)
	repeats_on = ndb.JsonProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year
	
	TimeUse_target_min = ndb.IntegerProperty()
	TimeUse_target_max = ndb.IntegerProperty()





