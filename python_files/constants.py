import operator

l_Fibonacci = [1,2,3,5,8,13]

l_long_Fibonacci = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]

l_Fibonacci_1_8 = [1,2,3,5,8]

l_Fibonacci_0_8 = [0,1,2,3,5,8]

l_Fibonacci_8_55 = [8,13,21,34,55]

l_Fibonacci_21_144 = [21,34,55,89,144]



d_KsuTypes = {
	'Gene': '00. Unassigned',
	'KeyA': '01. Key Action',
	# 'MinO': '02. Mini Objective',
	'BigO': '02. Objective',
	# 'Drea': '04. Dream',
	'Wish': '03. Wish',
	'EVPo': '05. End Value Trigger',
	'ImPe': '06. Important Person',
	'Idea': '07. Wise Idea',
	'RTBG': '08. Reason To Be Grateful',
	# 'Prin': '10. Principle',
	# 'NoAR': '11. Reminder',
	# 'MoRe': '12. Money Requirement',
	'ImIn': '09. Indicator'
}

l_KsuTypes = sorted(d_KsuTypes.items(), key=operator.itemgetter(1))

def removeNumbers(tupleList, start):
	result = []
	for e in tupleList:
		result.append((e[0],e[1][start:]))		
	return result

l_KsuTypes = removeNumbers(l_KsuTypes, 4)


def makeDictionaryFromTupleList(tupleList):
	result = {}
	for e in tupleList:
		result[e[0]] = e[1]		
	return result

d_KsuTypes = makeDictionaryFromTupleList(l_KsuTypes)

d_KsuSubtypes = {
	'KAS1or2':'Key Proactive Action',
	'KAS3': 'Key Reactive Action',
	'KAS4': 'Key Action To Avoid'
}


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

	'value_type':'string',
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

	'repeats_on_Mon':'check_repeats_on',
	'repeats_on_Tue':'check_repeats_on', 
	'repeats_on_Wed':'check_repeats_on',
	'repeats_on_Thu':'check_repeats_on',
	'repeats_on_Fri':'check_repeats_on',
	'repeats_on_Sat':'check_repeats_on',
	'repeats_on_Sun':'check_repeats_on',

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
	'is_sprint_goal':'checkbox',

	#Wish Specific
	'wish_categorie': 'string',
	'money_cost':'integer',
	'in_bucket_list':'checkbox',

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


constants = {'l_Fibonacci':l_Fibonacci,
			 'l_long_Fibonacci': l_long_Fibonacci,
			 'l_Fibonacci_1_8' :l_Fibonacci_1_8,
			 'l_Fibonacci_8_55':l_Fibonacci_8_55,
			 'l_Fibonacci_0_8':l_Fibonacci_0_8,
			 'l_Fibonacci_21_144':l_Fibonacci_21_144,
			 
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


			 