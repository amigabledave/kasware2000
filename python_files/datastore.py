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
 	day_start_time = ndb.TimeProperty()
 	kpts_goals_parameters = ndb.JsonProperty(required=True)
 	kpts_goals = ndb.JsonProperty(required=True)
 	categories = ndb.JsonProperty(required=True)
	
	#tracker fields
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	last_DailyLog = ndb.IntegerProperty(required=True)

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

	global_category = ndb.StringProperty()
	local_category = ndb.StringProperty()
	# parent_id = ndb.KeyProperty(kind=KSU) # Ahora me esta dando un error porque lo estoy ligando a la misma clase que estoy definiendo

	kpts_value = ndb.FloatProperty()
	is_special = ndb.BooleanProperty(default=False)
		
	is_active = ndb.BooleanProperty(default=True)
	is_critical = ndb.BooleanProperty(default=False)
	is_private = ndb.BooleanProperty(default=False)

	is_visible = ndb.BooleanProperty(default=True)
	in_graveyard = ndb.BooleanProperty(default=False)
	is_deleted = ndb.BooleanProperty(default=False)			

	next_event = ndb.DateProperty()
	pretty_next_event = ndb.StringProperty()
	frequency = ndb.IntegerProperty()
	repeats = ndb.StringProperty() # KAS1 Specific		
	repeats_on = ndb.JsonProperty() #Day's of the week when it repeats if the frequency is Weekly, elese the repetition date is the same day of the month or year
	best_time = ndb.TimeProperty()

	target = ndb.JsonProperty() # For ksus that generate kpts and indicators target min, target max, reverse target etc
	birthday = ndb.DateProperty()
	money_cost = ndb.IntegerProperty()
	# picture = ndb.BlobProperty() #Might be used in the future


class Event(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)
	ksu_id = ndb.KeyProperty(kind=KSU, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)

	# base properties
	user_date_date = ndb.DateTimeProperty(auto_now_add=True)	
	user_date = ndb.IntegerProperty(required=True)
	event_type = ndb.StringProperty(required=True)
	comments = ndb.TextProperty()

	#Score properties
	kpts_type = ndb.StringProperty()
	score = ndb.FloatProperty(default=0)


class DailyLog(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	
	#base properties	
	user_date_date = ndb.DateTimeProperty(required=True)
	user_date = ndb.IntegerProperty(required=True)
	diary_entry = ndb.TextProperty()
	
	goal_achieved = ndb.BooleanProperty(default=False)
	streak_start_date =  ndb.IntegerProperty(required=True) #An number that represents a date
	

	#Score properties
	Streak = ndb.IntegerProperty(default=0)
	Goal = ndb.FloatProperty(default=0)

	EffortReserve = ndb.FloatProperty(default=0)
	PointsToGoal = ndb.FloatProperty(default=0)
	
	SmartEffort = ndb.FloatProperty(default=0)
	Stupidity = ndb.FloatProperty(default=0)
	



### Might be used in the future
# class Tag(ndb.Model):
	
# 	theory = ndb.KeyProperty(kind=Theory, required=True)
# 	created = ndb.DateTimeProperty(auto_now_add=True)		
# 	last_modified = ndb.DateTimeProperty(auto_now=True)
	
# 	name = ndb.StringProperty(required=True)
# 	description = ndb.StringProperty()
# 	ksus = ndb.KeyProperty(kind=Theory, repeated=True)	#all KSUs related to this tag
