

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
	parent_id = ndb.KeyProperty(kind=KSU)

	kpts_value = ndb.FloatProperty()
	is_pinned = ndb.BooleanProperty(default=False)
		
	is_active = ndb.BooleanProperty(default=True)
	is_important = ndb.BooleanProperty(default=False)
	is_private = ndb.BooleanProperty(default=False)

	is_visible = ndb.BooleanProperty(default=True)
	is_deleted = ndb.BooleanProperty(default=False)
	in_graveyard = ndb.BooleanProperty(default=False)
			
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
	
	
	
kpts_value = [kpts_reward, kpts_punishment, awesomeness]

secondary_description = [trigger_circumstances, valid_exceptions, success_definition, trigger_action, source, question]

frequency = [repeats_every, charging_time, contact_frequency, question_frequency]

event_date = [next_event, target_date, next_trigger_event, next_contact_event]

pretty_event_date = [pretty_next_event, pretty_target_date]

birthday = [impe_birthday, awesome_since]

best_time = [best_time, question_time]

is_important = [is_critical, is_BigO, is_dream, is_principle, was_awesome]

