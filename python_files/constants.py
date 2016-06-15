import operator

l_Fibonacci = [1,2,3,5,8,13]

l_long_Fibonacci = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]

l_Fibonacci_1_8 = [1,2,3,5,8]

l_Fibonacci_8_55 = [8,13,21,34,55]

l_Fibonacci_21_144 = [21,34,55,89,144]



d_KsuTypes = {
	'Gene': '00. Unassigned',
	'KeyA': '01. Key Action',
	# 'MinO': '02. Mini Objective',
	'BigO': '03. Objective',
	'Drea': '04. Dream',
	'Wish': '05. Wish',
	'Prin': '06. Principle',
	'EVPo': '06. End Value',
	'ImPe': '08. Important People',
	'RTBG': '09. Reason To Be Grateful',
	'Idea': '10. Wise Idea',
	'NoAR': '11. Reminder',
	'MoRe': '12. Money Requirement',
	'ImIn': '13. Indicator'
}

l_KsuTypes = sorted(d_KsuTypes.items(), key=operator.itemgetter(1))

def removeNumbers(tupleList):
	result = []
	for e in tupleList:
		result.append((e[0],e[1][4:]))		
	return result

l_KsuTypes = removeNumbers(l_KsuTypes)


def makeDictionaryFromTupleList(tupleList):
	result = {}
	for e in tupleList:
		result[e[0]] = e[1]		
	return result

d_KsuTypes = makeDictionaryFromTupleList(l_KsuTypes)

print d_KsuTypes


d_Values = {'V00': '0. End Value',
			'V01': '1. Inner Peace & Consciousness',
			'V02': '2. Fun & Exciting Situations', 
			'V03': '3. Meaning & Direction', 
			'V04': '4. Health & Vitality', 
			'V05': '5. Love & Friendship', 
			'V06': '6. Knowledge & Skills', 
			'V07': '7. Outer Order & Peace', 
			'V08': '8. Stuff',
		 	'V09': '9. Money & Power'}
l_Values = sorted(d_Values.items())


d_Mean_Values = {'V01': '1. Inner Peace & Consciousness',
			 	'V02': '2. Fun & Exciting Situations', 
				'V03': '3. Meaning & Direction', 
				'V04': '4. Health & Vitality', 
				'V05': '5. Love & Friendship', 
				'V06': '6. Knowledge & Skills', 
				'V07': '7. Outer Order & Peace', 
				'V08': '8. Stuff',
			 	'V09': '9. Money & Power'}
l_Mean_Values = sorted(d_Mean_Values.items())


d_Scope = {'Total': 'Overall Results',
		   'V000': '0. End Value',
		   'V100': '1. Inner Peace & Consciousness',
		   'V200': '2. Fun & Exciting Situations', 
		   'V300': '3. Meaning & Direction', 
		   'V400': '4. Health & Vitality', 
		   'V500': '5. Love & Friendship', 
		   'V600': '6. Knowledge & Skills', 
	       'V700': '7. Outer Order & Peace', 
	       'V800': '8. Stuff',
		   'V900': '9. Money & Power'}
l_Scope = sorted(d_Scope.items())


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
	'target_date': 'date'
}


d_repeats_legend = {
	'R000':'',
	'R001':'Days',
	'R007':'Weeks',
	'R030':'Months',
	'R365':'Years'}




constants = {'l_Fibonacci':l_Fibonacci,
			 'l_long_Fibonacci': l_long_Fibonacci,
			 'l_Fibonacci_1_8' :l_Fibonacci_1_8,
			 'l_Fibonacci_8_55':l_Fibonacci_8_55,
			 'l_Fibonacci_21_144':l_Fibonacci_21_144,
			 'l_KsuTypes':l_KsuTypes, 
			 'l_Values':l_Values,
			 'l_Mean_Values':l_Mean_Values,
			 'l_Days':l_Days,
			 'l_repeats':l_repeats,
			 'd_KsuTypes':d_KsuTypes,
			 'd_attributeType':d_attributeType,
			 'd_repeats_legend':d_repeats_legend}


			 