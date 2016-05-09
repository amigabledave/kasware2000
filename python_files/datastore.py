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


class Tag(db.Model):
	
	theory = db.ReferenceProperty(Theory, collection_name='Tags')
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)
	
	name = db.StringProperty(required=True)
	description = db.StringProperty()

	ksus = db.ListProperty(db.Key) 	#all KSUs related to this tag



class KSU(db.Model):
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)

	# base KSU properties
	description = db.StringProperty(required=True)
	status = db.StringProperty(choices=('Active', 'Done', 'Hold', 'Deleted'))

	# theory = db.ReferenceProperty(Theory, collection_name='KSUs')	#Included on last level
	# ksu_type = db.StringProperty(required=True) #Included on last level
	# ksu_id = db.StringProperty(required=True) #Not sure if with the new datastore structure is really necesary

	ksu_subtype = db.StringProperty()
	parent_id = db.StringProperty()	
			
	is_visible = db.BooleanProperty(default=True)
	is_private = db.BooleanProperty(default=False)

	tags = db.ListProperty(db.Key) #all tags related to this KSU	
	comments = db.TextProperty()
	picture = db.BlobProperty()

	value_type = db.StringProperty(required=True, choices=('V00','V09', 'V10', 'V20', 'V30', 'V40', 'V50', 'V60', 'V70', 'V80', 'V90'), default='V09')
	importance = db.IntegerProperty(default=3)
	is_critical = db.BooleanProperty(default=False)



class KAS(KSU):
			
	in_mission = db.BooleanProperty(default=False)
	any_any = db.BooleanProperty(default=False)
	in_upcoming = db.BooleanProperty(default=True)

	next_event = db.DateProperty(required=False)
	best_time = db.TimeProperty()
	time_cost = db.IntegerProperty(default=1)

	Repetition_target_min = db.IntegerProperty()
	Repetition_target_max = db.IntegerProperty()

	project = db.StringProperty()



class KAS1(KAS):
		
	theory = db.ReferenceProperty(Theory, collection_name='KAS1', required=True)
	ksu_type = db.StringProperty(default='KAS1') 
	
	last_event = db.DateProperty()
	repeats = db.StringProperty(required=True, choices=('R001', 'R007', 'R030', 'R365'))	
	repeats_every = db.IntegerProperty(required=True, default=1)
	repeats_on = db.StringListProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year
	
	TimeUse_target_min = db.IntegerProperty()
	TimeUse_target_max = db.IntegerProperty()





