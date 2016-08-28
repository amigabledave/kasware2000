from google.appengine.ext import ndb

#--- datastore classes ----------

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
 	timezone = ndb.IntegerProperty(default=-4) #Deberia de ser forzoza, pero para evitar errores por ahora no la solicito asi
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
	kpts_value = ndb.FloatProperty()

	importance = ndb.IntegerProperty(default=3)
	mission_importance = ndb.IntegerProperty(default=3)
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
	best_time = ndb.TimeProperty()
	pretty_best_time = ndb.StringProperty()

	target = ndb.JsonProperty() # For ksus that generate kpts and indicators target min, target max, reverse target etc
	birthday = ndb.DateProperty()
	money_cost = ndb.IntegerProperty()
	picture = ndb.BlobProperty() #Might be used in the future
	times_reviewed = ndb.IntegerProperty(default=0)


class Event(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)
	ksu_id = ndb.KeyProperty(kind=KSU, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	is_deleted = ndb.BooleanProperty(default=False)

	# base properties
	user_date_date = ndb.DateTimeProperty(auto_now_add=True)	
	user_date = ndb.IntegerProperty(required=True)
	event_type = ndb.StringProperty(required=True)
	
	comments = ndb.TextProperty()
	secondary_comments = ndb.StringProperty()
	is_private = ndb.BooleanProperty(default=False)
	importance = ndb.IntegerProperty(default=3)

	#Score properties
	kpts_type = ndb.StringProperty()
	score = ndb.FloatProperty(default=0)

	#KSU properties
	ksu_description = ndb.StringProperty()	
	ksu_subtype = ndb.StringProperty()
	ksu_tags = ndb.StringProperty()


class DailyLog(ndb.Model):

	#tracker fields
	theory = ndb.KeyProperty(kind=Theory, required=True)	
	created = ndb.DateTimeProperty(auto_now_add=True)	
	last_modified = ndb.DateTimeProperty(auto_now=True)
	
	user_date_date = ndb.DateTimeProperty(required=True)
	user_date = ndb.IntegerProperty(required=True)
	
	#Score properties
	goal_achieved = ndb.BooleanProperty(default=False)
	streak_start_date =  ndb.IntegerProperty(required=True) #An number that represents a date

	Streak = ndb.IntegerProperty(default=0)
	Goal = ndb.FloatProperty(default=0)

	EffortReserve = ndb.FloatProperty(default=0)
	PointsToGoal = ndb.FloatProperty(default=0)
	
	SmartEffort = ndb.FloatProperty(default=0)
	Stupidity = ndb.FloatProperty(default=0)

	

#--- Validation and security functions ----------
import hashlib, random

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



### Might be used in the future
# class Tag(ndb.Model):
	
# 	theory = ndb.KeyProperty(kind=Theory, required=True)
# 	created = ndb.DateTimeProperty(auto_now_add=True)		
# 	last_modified = ndb.DateTimeProperty(auto_now=True)
	
# 	name = ndb.StringProperty(required=True)
# 	description = ndb.StringProperty()
# 	ksus = ndb.KeyProperty(kind=Theory, repeated=True)	#all KSUs related to this tag
