import operator

def removeNumbers(tupleList, start):
	result = []
	for e in tupleList:
		result.append((e[0],e[1][start:]))		
	return result

def makeDictionaryFromTupleList(tupleList):
	result = {}
	for e in tupleList:
		result[e[0]] = e[1]		
	return result


l_Fibonacci = [1,2,3,5,8,13]

l_long_Fibonacci = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]

l_Fibonacci_1_8 = [1,2,3,5,8]

l_Fibonacci_0_8 = [0,1,2,3,5,8]

l_Fibonacci_8_55 = [8,13,21,34,55]

l_Fibonacci_21_144 = [21,34,55,89,144]


default_ksu = {}

# default_ksu = {
# 	'ksu_type':'KeyA',
# 	'ksu_subtype':'KAS2',
# 	'repeats':'R000',
# 	'repeats_on': {
# 		'repeats_on_Mon': False,
# 		'repeats_on_Tue': False, 
# 		'repeats_on_Wed': False, 
# 		'repeats_on_Thu': False,
# 		'repeats_on_Fri': False,
# 		'repeats_on_Sat': False,
# 		'repeats_on_Sun': False},
# } 



d_SetTitles = {
	'Gene': 'Unassigned KSUs',
	'KeyA': 'Key Actions Set',
	# 'MinO': '02. Mini Objective',
	'BigO': 'Objectives',
	# 'Drea': '04. Dream',
	'Wish': 'Wishes',
	'EVPo': 'End Value Mines',
	'ImPe': 'Important People',
	'Idea': 'Wise Ideas',
	'RTBG': 'Reasons To Be Grateful',
	# 'Prin': '10. Principle',
	# 'NoAR': '11. Reminder',
	# 'MoRe': '12. Money Requirement',
	'ImIn': 'Indicator'}


d_KsuTypes = {
	'Gene': '00. Unassigned',
	'KeyA': '01. Key Action',
	# 'MinO': '02. Mini Objective',
	'BigO': '02. Objective',
	# 'Drea': '04. Dream',
	'Wish': '03. Wish',
	'EVPo': '05. End Value Mine',
	'ImPe': '06. Important Person',
	'Idea': '07. Wise Idea',
	'RTBG': '08. Reason To Be Grateful',
	# 'Prin': '10. Principle',
	# 'NoAR': '11. Reminder',
	# 'MoRe': '12. Money Requirement',
	'ImIn': '09. Indicator'}
l_KsuTypes = sorted(d_KsuTypes.items(), key=operator.itemgetter(1))
l_KsuTypes = removeNumbers(l_KsuTypes, 4)
d_KsuTypes = makeDictionaryFromTupleList(l_KsuTypes)

d_KsuSubtypes = {
	'Gene':'Unassigned',
	'KeyA':'Key Action',
	'KAS1':'Key Repetitive Action',
	'KAS2':'Key Action',
	'KAS3':'Key Reaction',
	'KAS4':'Key Action To Avoid',

	'BigO': 'Big Objective',
	
	'MinO': 'Sprint Goal',

	'Wish': 'Wish',

	'Dream': 'Dream',

	'EVPo': 'End Value Mine',

	'ImPe': 'Important Person',

	'Idea': 'Wise Idea',
	'Principle': 'Principle',

	'RTBG': 'Reason To Be Grateful',

	'ImIn': 'Indicator',
	'RealitySnapshot':'Reality Indicator',
	'AcumulatedPerception': 'Perception Indicator'} 

d_ValueTypes = {
	'V01': '0. Unassigned',
	'V10': '1. Inner Peace & Consciousness',
	'V20': '2. Fun & Exciting Situations', 
	'V30': '3. Meaning & Direction', 
	'V40': '4. Health & Vitality', 
	'V50': '5. Love & Friendship', 
	'V60': '6. Knowledge & Skills', 
	'V70': '7. Outer Order & Peace', 
	'V80': '8. Stuff',
	'V90': '9. Money & Power'}
l_ValueTypes = sorted(d_ValueTypes.items())

d_ValueTypes = makeDictionaryFromTupleList(removeNumbers(l_ValueTypes, 3))


d_repeats = {'R000':'Never',
			 'R001':'Daily',
			 'R007':'Weekly',
			 'R030':'Monthly',
			 'R365':'Yearly'}
l_repeats = sorted(d_repeats.items())


d_Days = {'None':'None',
		  '1':'1. Sunday',
		  '2':'2. Monday',
		  '3':'3. Tuesday',
		  '4':'4. Wednesday',
		  '5':'5. Thursday',
		  '6':'6. Friday',
		  '7':'7. Saturday'}
l_Days = sorted(d_Days.items())


d_attributeType = {
	'description':'string',
	'comments':'string',
	'ksu_type':'string',
	'ksu_subtype':'string',

	'global_category':'string',
	'local_category':'string',
	# 'tags':'', Assignment pending
	# 'parent_id':'', Assignment pending		
		
	'is_active': 'checkbox',
	'is_critical': 'checkbox',
	'is_private': 'checkbox',

	# 'is_visible':'Checkbox', These are not input attributes
	# 'is_deleted':'Checkbox',

	# base properties - might be used in the future
	# 'picture':'', Assignment pending
	'importance':'integer',
			
	# KAS Specific	
	'last_event':'date',
	'next_event':'date',
	
	'best_time':'time',
	'time_cost':'integer',

	'repeats':'string',	
	'repeats_every':'integer',

	'repeats_on_Mon':'checkbox_repeats_on',
	'repeats_on_Tue':'checkbox_repeats_on', 
	'repeats_on_Wed':'checkbox_repeats_on',
	'repeats_on_Thu':'checkbox_repeats_on',
	'repeats_on_Fri':'checkbox_repeats_on',
	'repeats_on_Sat':'checkbox_repeats_on',
	'repeats_on_Sun':'checkbox_repeats_on	',

	'trigger_circumstances':'string',
	'standard_reward':'integer',
	'valid_exceptions':'string',
	'standard_punishment':'integer',

	# KAS Specific - might be used in the future
	# 'Repetition_target_min':'integer',
	# 'Repetition_target_max':'integer',
	# 'TimeUse_target_min': 'integer',
	# 'TimeUse_target_max': 'integer',

	#Objective Specific
	'success_definition': 'string',
	'target_date': 'date',
	'is_BigO':'checkbox',

	#Wish Specific
	'wish_categorie': 'string',
	'money_cost':'integer',
	'is_dream':'checkbox',

	#EVPo Specific
	'charging_time': 'integer',
	'trigger_action': 'string',
	'next_trigger_event': 'date',

	#Idea Specific
	'source': 'string',
	'is_principle':'checkbox',

	#Important Person Specific
	'contact_frequency': 'integer',
	'contact_action': 'string',
	'next_contact_event': 'date',
	'impe_birthday': 'date',
	# 'impe_kaswareID': 'string' - 	To be used in the future

	#RTBG Specific
	'awesomeness': 'integer',
	# 'max_awesomeness = ndb.IntegerProperty() # To be used to track max awesomeness
	'was_awesome':  'checkbox',
	'awesome_since': 'date',

	#Indicator Specifics
	'question': 'string',
	'question_time': 'string',
	'question_frequency': 'integer',
	'target_max':'float',
	'target_min': 'float',
	'reverse_target':'checkbox'
	}


d_repeats_legend = {
	'R000':'',
	'R001':'Days',
	'R007':'Weeks',
	'R030':'Months',
	'R365':'Years'}


d_local_categories = {
	'Gene': ['Unassigned'],
	'KeyA': ['Unassigned'],
	'BigO': ['Unassigned'],
	'Wish': [	
		'Unassigned',	
		'01. Being',
		'02. Having',
		'03. Doing',
		'04. Geting done',
		'05. TV Show',
		'06. Movie',
		'07. Tesis',
		'08. Novel',
		'09. Video Game',
		'10. Board Game',
		'11. City'],	
	'Prin': ['Unassigned'],
	'EVPo': ['Unassigned'],
	'ImPe': ['Unassigned'],
	'RTBG': ['Unassigned'],
	'Idea': ['Unassigned'],
	'NoAR': ['Unassigned'],
	'MoRe': ['Unassigned'],
	'ImIn': ['Unassigned']}


d_SetViewerDetails = {
	
	'Gene':{},

	'KeyA':{},

	'KAS1':{
		'attributes': ['next_event', 'repeats'],
		'fields': {'next_event':'Next Event', 'repeats':'Repeats'},
		'columns':{'next_event':3, 'repeats':3},
		'buttons':['Done', 'SendToMission']},

	'KAS2':{		
		'attributes': ['pretty_next_event'],
		'fields': {'pretty_next_event':'Scheduled for'},
		'columns':{'pretty_next_event':6},
		'buttons':['Done', 'SendToMission']},

	'KAS3':{
		'attributes': ['standard_reward'],
		'fields': {'standard_reward':'Standard Reward (kpts.)'},
		'columns': {'standard_reward':6},
		'buttons': ['Done', 'PinInMission']},

	'KAS4':{
		'attributes': ['standard_punishment'],
		'fields': {'standard_punishment':'Standard Punishment (kpts.)'},
		'columns':{'standard_punishment':6},
		'buttons':['Done', 'PinInMission']},

	'BigO':{		
		'attributes': ['pretty_target_date'],
		'fields': {'pretty_target_date':'Target Date'},
		'columns':{'pretty_target_date':6},
		'buttons':['Done', 'PinInMission']},

	'MinO':{		
		'attributes': ['pretty_target_date'],
		'fields': {'pretty_target_date':'Target Date'},
		'columns':{'pretty_target_date':6},
		'buttons':['Done', 'PinInMission']},

	'Wish':{ 		
		'attributes': ['money_cost'],
		'fields': {'money_cost':'Money required ($)'},
		'columns':{'money_cost':6},
		'buttons':['Done', 'PinInMission']},

	'Dream':{ 		
		'attributes': ['money_cost'],
		'fields': {'money_cost':'Money required ($USD)'},
		'columns':{'money_cost':6},
		'buttons':['Done', 'PinInMission']},

	'EVPo': { 		
		'attributes': ['charging_time'],
		'fields': {'charging_time':'Charging time (days)'},
		'columns':{'charging_time':6},
		'buttons':['Done', 'PinInMission']},

	'ImPe': { 		
		'attributes': ['contact_frequency'], 
		'fields': {'contact_frequency':'Contact Frequency (days)'},
		'columns':{'contact_frequency':6},
		'buttons':['Done', 'SendToMission']},

	'Idea': { 		
		'attributes': ['source'],
		'fields': {'source':'Source'},
		'columns':{'source':6},
		'buttons':['Done', 'PinInMission']},

	'Principle': { 		
		'attributes': ['source'],
		'fields': {'source':'Source'},
		'columns':{'source':6},
		'buttons':['Done', 'PinInMission']},

	'RTBG': { 		
		'attributes': ['awesomeness'],
		'fields': {'awesomeness':'Added Awesomeness'},
		'columns':{'awesomeness':6},
		'buttons':['Done', 'PinInMission']},

	'ImIn': { 		
		'attributes': [], 
		'fields': {},
		'columns':{},
		'buttons':['Done', 'PinInMission']},

	'AcumulatedPerception': { 		
		'attributes': [], 
		'fields': {},
		'columns':{},
		'buttons':['Done', 'PinInMission']},

	'RealitySnapshot': { 		
		'attributes': [], 
		'fields': {},
		'columns':{},
		'buttons':['Done', 'PinInMission']},
}


l_attributesThatNeedToBeFixed = ['repeats']

d_displayValues = {}
d_displayValues.update(d_repeats)

constants = {'l_Fibonacci':l_Fibonacci,
			 'l_long_Fibonacci': l_long_Fibonacci,
			 'l_Fibonacci_1_8' :l_Fibonacci_1_8,
			 'l_Fibonacci_8_55':l_Fibonacci_8_55,
			 'l_Fibonacci_0_8':l_Fibonacci_0_8,
			 'l_Fibonacci_21_144':l_Fibonacci_21_144,
			 
			 'default_ksu':default_ksu,

			 'd_SetTitles':d_SetTitles,
			 'l_attributesThatNeedToBeFixed':l_attributesThatNeedToBeFixed,
			 'd_displayValues':d_displayValues,
			 'd_SetViewerDetails':d_SetViewerDetails,

			 'd_KsuTypes':d_KsuTypes,
			 'l_KsuTypes':l_KsuTypes,
			 'd_KsuSubtypes':d_KsuSubtypes, 
			 'd_ValueTypes':d_ValueTypes,
			 'l_ValueTypes':l_ValueTypes,
			 
			 'l_Days':l_Days,
			 'd_repeats': d_repeats,
			 'l_repeats':l_repeats,
			 'd_repeats_legend':d_repeats_legend,

			 'd_attributeType':d_attributeType,
			 'd_local_categories':d_local_categories}


			 