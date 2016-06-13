#Have not finished working on input validation so far.

d_validationMethod ={
	'description':'RE',
	'comments':'RE',
	'ksu_type':'List',
	'ksu_subtype':'List',

	'value_type':'List',
	# 'tags':'', Assignment pending
	# 'parent_id':'', Assignment pending		
		
	'is_active': 'Checkbox',
	'is_critical': 'Checkbox',
	'is_private': 'Checkbox',

	'is_visible':'Checkbox',
	'is_deleted':'Checkbox',

	# base properties - might be used in the future
	# 'picture':'', Assignment pending
	'importance':'RE',
			
	# KAS Specific	
	'last_event':'Date',
	'next_event':'Date',
	
	'best_time':'Time',
	'time_cost':'RE',

	'repeats':'List',	
	'repeats_every':'RE',

	'repeats_on_Mon':'Checkbox',
	'repeats_on_Tue':'Checkbox', 
	'repeats_on_Wed':'Checkbox',
	'repeats_on_Thu':'Checkbox',
	'repeats_on_Fri':'Checkbox',
	'repeats_on_Sat':'Checkbox',
	'repeats_on_Sun':'Checkbox',

	'trigger_circumstances':'TextProperty',
	'standard_reward':'IntegerProperty',
	'valid_exceptions':'TextProperty',
	'standard_punishment':'IntegerProperty',

	# KAS Specific - might be used in the future
	'Repetition_target_min':'IntegerProperty',
	'Repetition_target_max':'IntegerProperty',
	'TimeUse_target_min': 'IntegerProperty',
	'TimeUse_target_max': 'IntegerProperty'
}



d_howToValidate = {
	'StringProperty': 'RegularExpression',
	'TextProperty':,
	'KeyProperty':,

	'BooleanProperty':
	'BlobProperty':,
	'IntegerProperty':'RegularExpression',

	'DateProperty':
	'TimeProperty':
	'JsonProperty()':

}




d_dataTypeToRE = {

}



d_inputToDataType ={
	'description':'StringProperty'
	'comments':'TextProperty',
	'ksu_type':'StringProperty',
	'ksu_subtype':'StringProperty',

	'value_type':'StringProperty',
	'tags':'KeyProperty',
	'parent_id':'StringProperty',		
		
	'is_active': 'BooleanProperty',
	'is_critical': 'BooleanProperty',
	'is_private':'BooleanProperty',

	'is_visible':'BooleanProperty',
	'is_deleted':'ndb.BooleanProperty',

	# base properties - might be used in the future
	'picture':'BlobProperty',
	'importance':'IntegerProperty',
			
	# KAS Specific	
	'last_event':'DateProperty',
	'next_event':'DateProperty',
	
	'best_time':'TimeProperty',
	'time_cost':'IntegerProperty',

	'repeats':'StringProperty',	
	'repeats_every':'IntegerProperty',
	'repeats_on':'JsonProperty()', 

	'trigger_circumstances':'TextProperty',
	'standard_reward':'IntegerProperty',
	'valid_exceptions':'TextProperty',
	'standard_punishment':'IntegerProperty',

	# KAS Specific - might be used in the future
	'Repetition_target_min':'IntegerProperty',
	'Repetition_target_max':'IntegerProperty',
	'TimeUse_target_min': 'IntegerProperty',
	'TimeUse_target_max': 'IntegerProperty'
}



validation_attributes =[
	
	#KSU Attributes
	'description',
	'comments',
	'ksu_type',
	'ksu_subtype',

	'value_type',
	'tags',
	'parent_id',		
		
	'is_active': 'BooleanProperty',
	'is_critical': 'BooleanProperty',
	'is_private':'BooleanProperty',

	'is_visible':'BooleanProperty',
	'is_deleted':'ndb.BooleanProperty',

	# base properties - might be used in the future
	'picture':'BlobProperty',
	'importance':'IntegerProperty',
			
	# KAS Specific	
	'last_event':'DateProperty',
	'next_event':'DateProperty',
	
	'best_time':'TimeProperty',
	'time_cost':'IntegerProperty',

	'repeats':'StringProperty',	
	'repeats_every':'IntegerProperty',
	'repeats_on':'JsonProperty()', 

	'trigger_circumstances':'TextProperty',
	'standard_reward':'IntegerProperty',
	'valid_exceptions':'TextProperty',
	'standard_punishment':'IntegerProperty',

	# KAS Specific - might be used in the future
	'Repetition_target_min':'IntegerProperty',
	'Repetition_target_max':'IntegerProperty',
	'TimeUse_target_min': 'IntegerProperty',
	'TimeUse_target_max': 'IntegerProperty'
]






def input_error(target_attribute, user_input):
	
	validation_attributes = ['username', 
							 'password',
							 'email',
							 'birthday',
							 'description',
							 'short_description',
							 'charging_time',
							 'time_cost',
							 'contact_frequency',
							 'question_frequency',
							 'duration',
							 'repetitions', 
							 'last_event', 
							 'next_event', 
							 'target_date', 
							 'comments', 
							 'period_end',
							 'period_duration',
							 'money_cost',
							 'numeric_answer']

	date_attributes = ['last_event', 'next_event', 'target_date', 'period_end', 'milestone_target_date', 'birthday']

	if target_attribute not in validation_attributes:
		return None
	error_key = target_attribute + '_error' 
		
	if target_attribute in date_attributes:
		if valid_date(user_input):
			return None
		else:
			return d_RE[error_key]

	elif d_RE[target_attribute].match(user_input):
		return None
	
	else:
		return d_RE[error_key]



d_RE = {'username': re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
		'username_error': 'Invalid Username Syntax',
		
		'password': re.compile(r"^.{3,20}$"),
		'password_error': 'Invalid Password Syntax',
		
		'email': re.compile(r'^[\S]+@[\S]+\.[\S]+$'),
		'email_error': 'Invalid Email Syntax',

		'description': re.compile(r"^.{3,200}$"),
		'description_error': 'Description max lenght is 200 characters and min 3.',

		'short_description': re.compile(r"^.{3,30}$"),
		'short_description_error': 'Short description max lenght is 30 characters and min 3.',

		'charging_time': re.compile(r"^[0-9]{1,3}$"),
		'charging_time_error': 'Charging Time should be an integer with maximum 3 digits',

		'time_cost': re.compile(r"^[0-9]{1,3}$"),
		'time_cost_error': 'Time cost should be an integer with maximum 3 digits',

		'duration': re.compile(r"^[0-9]{1,3}$"),
		'duration_error': 'Duration should be an integer with maximum 3 digits',

		'question_frequency': re.compile(r"^[0-9]{1,3}$"),
		'question_frequency_error': 'Question Frequency should be an integer',

		'contact_frequency': re.compile(r"^[0-9]{1,3}$"),
		'contact_error': 'contact_frequency should be an integer with maximum 3 digits',		

		'money_cost': re.compile(r"^[0-9]{1,12}$"),
		'money_cost_error': 'The money cost should be an integer',

		'repetitions': re.compile(r"^[0-9]{1,3}$"),
		'repetitions_error': "Repetitions should be an integer",

		'period_duration': re.compile(r"^[0-9]{1,3}$"),
		'period_duration_error': "Period's duration should be an integer",

		'birthday_error':'Birthday format must be DD-MM-YYYY',
		'last_event_error':'Last event format must be DD-MM-YYYY',
		'next_event_error':'Next event format must be DD-MM-YYYY',
		'target_date_error':'Target date format must be DD-MM-YYYY',
		'period_end_error':"Period's End format must be DD-MM-YYYY",
		'milestone_target_date_error':"Period's End format must be DD-MM-YYYY",

		'comments': re.compile(r"^.{0,1000}$"),
		'comments_error': 'Comments cannot excede 1,000 characters',
		
		'numeric_answer':re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"),
		'numeric_answer_error':'The answer should be a number'}

