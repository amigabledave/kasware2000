from google.appengine.ext import db


class Theory(db.Model):

	#login details		
	username = db.StringProperty(required=True)
	password_hash = db.StringProperty(required=True)
	
	#user details	
	email = db.EmailProperty(required=True)
	owner = db.StringProperty() #ID of user that owns this theory. Esto lo voy usar cuando permita log-in con una cuenta de Google
	
 	#user settings
 	language = db.StringProperty(choices=('Español', 'English'), default='English')
 	hide_private_ksus = BooleanProperty(default=False)
	
	#tracker fields
	created = db.DateTimeProperty(auto_now_add=True)	
	last_modified = db.DateTimeProperty(auto_now=True)



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
	local_tags = db.ListProperty(db.Key) #all global tags related to this KSU	
	origin = db.TextProperty() #Quien lo recomendo o como fue que este KSU llego a mi teoria
	comments = db.TextProperty()
	picture = db.BlobProperty()

	#KAS KSU propeties
	value_type = db.StringProperty(required=True, choices=('V000', 'V100', 'V200', 'V300', 'V400', 'V500', 'V600', 'V700', 'V800', 'V900'))
	importance = db.IntegerProperty(choices=(1,2,3,5,8,13), default=3)
	is_critical = db.BooleanProperty(default=False)

	#proactive KAS KSU
	time_cost = db.IntegerProperty(default=1)
	next_event = db.DateProperty(required=True)
	best_time = db.TimeProperty()

	in_mission = db.BooleanProperty(default=False)
	any_any = db.BooleanProperty(default=False)
	in_upcoming = db.BooleanProperty(default=True)
	
	# KAS1 specifics
	charging_time = db.IntegerProperty(required=True)
	last_event = db.DateProperty()
	project = db.StringProperty()
	best_day = db.StringProperty()

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



