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


l_Fibonacci = [0.25,1,2,3,5,8,13]
d_attributeType = {

	'description':'string',
	'secondary_description':'string',

	'comments':'string',
	'ksu_type':'string',
	'ksu_subtype':'string',

	'global_category':'string',
	'local_category':'string',
	'parent_id':'ndb_key', 		

	'kpts_value':'float',
	'is_special':'checkbox',

	'is_active': 'checkbox',
	'is_critical': 'checkbox',
	'is_private': 'checkbox',

	'next_event':'date',
	'frequency':'integer',

	'repeats':'string',		
	'repeats_on_Mon':'checkbox_repeats_on',
	'repeats_on_Tue':'checkbox_repeats_on', 
	'repeats_on_Wed':'checkbox_repeats_on',
	'repeats_on_Thu':'checkbox_repeats_on',
	'repeats_on_Fri':'checkbox_repeats_on',
	'repeats_on_Sat':'checkbox_repeats_on',
	'repeats_on_Sun':'checkbox_repeats_on',
	'best_time':'time',

	# 'target':'tbd', # its a json For ksus that generate kpts and indicators target min, target max, reverse target etc
	'birthday': 'date',
	'money_cost': 'integer'
	}
default_ksu = {}
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
	'BinaryPerception': 'Binary Perception Indicator',
	'FibonacciPerception': 'Fibonacci Perception Indicator'} 

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
d_repeats_legend = {
	'R000':'',
	'R001':'Days',
	'R007':'Weeks',
	'R030':'Months',
	'R365':'Years'}


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
		'attributes': ['kpts_value'],
		'fields': {'kpts_value':'Reward (Kpts.)'},
		'columns': {'kpts_value':6},
		'buttons': ['Done', 'PinInMission']},

	'KAS4':{
		'attributes': ['kpts_value'],
		'fields': {'kpts_value':'Punishment (Kpts.)'},
		'columns':{'kpts_value':6},
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
		'buttons':['PinInMission']},

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

	'BinaryPerception': { 		
		'attributes': [], 
		'fields': {},
		'columns':{},
		'buttons':['Done', 'PinInMission']},

	'FibonacciPerception': { 		
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
			 'd_attributeType':d_attributeType,
			 'default_ksu':default_ksu,
			 'd_SetTitles':d_SetTitles,

			 'd_KsuTypes':d_KsuTypes,
			 'l_KsuTypes':l_KsuTypes,
			 'd_KsuSubtypes':d_KsuSubtypes, 

			 'd_repeats': d_repeats,
			 'l_repeats':l_repeats,

			 'l_Days':l_Days,
			 'd_repeats_legend':d_repeats_legend,
			 
			 'd_SetViewerDetails':d_SetViewerDetails,
			 'l_attributesThatNeedToBeFixed':l_attributesThatNeedToBeFixed,
			 'd_displayValues':d_displayValues}


			 