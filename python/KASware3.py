# Meter attributo nuevo en {MasterKSU.html:[], KASware3.py: [ksu_type_attributes, attributes_guide], KASware3app.js: [ksu_type_attributes, attributes_guide],}


ksu_types = [

	#Actions	
	[['Action', 'Action'], [
		['Proactive', 'Proactive', True],
		['Reactive', 'Reactive', ''],
		['Negative', 'Negative', '']
	]],	

	[['Objective', 'Mile Stone'], [ #Group actions in a well define purpose
		['Objective', 'Objective', True], #If the parent is another objective then its a milestone#'Milestone',
	]],
	
	[['Wisdom', 'Wisdom'], [#Idea #Your personal constitution. Non actionable knowledge that you believe should guide your behaviour.
		['Idea', 'Idea', True], #If the idea has a parent then is not a principle. BRILIANT!
		['Principle', 'Principle', ''], #Sirve para organizar y auditar
		['Learning', 'Learning', '']
	]], 
		
	#Life Pieces
	[['Experience', 'Experience'], [#What do you want to be doing? #'Surroundings = Aqui entra estar viviendo en Canada
		['Moment', 'Moment', True], # Whaterver < Nice < Very nice < Memorable < Epic < Legendary		
		['JoyMine', 'Joy Mine', ''], #Algo concreto que genera momentos del mismo tipo... E.g. Estar jugando Zelda breath of the wild
		['Chapter', 'Chapter', ''], #Agrupa varios momentos, pero no es un momento en si por lo que no tiene importancia. El padre puede ser otro chapter .E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild
		#'Experience' #If the parent is other joy generator, then its a generator instance: E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild	
	]],

	[['Contribution', 'Contribution'], [ #Whats the impact you want to have in others peoples life and the envieronment? Antes Meaning GreaterGood
		['Contribution', 'Contribution', True] #  #'Social', 'Environment',		
	]],
	
	[['SelfAttribute', 'Attribute'], [# Antes Self. #Who is the best person you could be? 'Antes tenia Achievemnt pero ahora queda en meaning',
		['Attitude', 'Attitude', ''], #'SoulSkill', #Connciousness and inner peace
		['KnowledgeOrSkill', 'Skill or Knowledge', True], #MindSkill Knowledge and skills		
		['BodyFeature', 'Body Feature', ''], #PhisicalAttribute, Health and vitality
		# ['Achievement', 'Achievement', ''] #Personal achievement.
	]],

	[['Person', 'Person'], [ #Who you want in your life 'Love', #Important People. Love & Friendship
		['Individual', 'Individual', True], #Person #If the parent is another person, then the parent is a group of people #'Group',
		['Group', 'Group', ''],
		['Role', 'Role'], #En el momento que se ancla a una persona se marca como realized. E.g. Sexual Partner, Someone to Play Magic, Etc...
	]],

	[['Possesion', 'Possesion'], [ #What you want to have
		['Thing', 'Thing', True], #For personal use #Tambien entra orden aqui. e.g. "Tener un cuarto ordenado"		
		['Service', 'Service Access'],
		['Asset', 'Asset', ''], #Dinero o assets tangibles. MoneyOrAsset
	]],	

	[['Situation', 'Situation'], [ #Whats the impact you want to have in others peoples life and the envieronment? Antes Meaning GreaterGood
		['SocialStatus', 'Social Status', True], #Aqui entrarian los trabajos o cualquier cosa que viva en las mentes de otras personas	
		['Environment', 'Environment', ''], #Aqui entra el lugar donde quieres vivir a nivel pais, hogar o cualquier escala
	]],

	#Indicator Results The concreate metrics you pick to measure success
	[['Indicator', 'Indicator'], [
		['Reality', 'Reality', ''],
		['Perception', 'Perception', True],
		# ['TernaryPerception', ],
	]],
]



event_types = {
	'EndValue', #Generado por momentos de Joy Generatos
	
	'Effort', #Generado por acciones al ser ejecutadas
	
	'Stupidity', #Generado por acciones al ser ejecutadas	
	
	'Progress', #Generado por objetivos
	
	'WishRealized',# Generado por Life Pieces al cambiar de status 	

	'Measurement', #Generaddo por indicadores
}


attributes_guide = {
	'theory_id': ['Key', ''], 	
	'created': ['DateTime', ''], 
	'ksu_type': ['String', 'Standard'],
	'ksu_subtype': ['String', 'Select'],
	'reason_id': ['Key', 'Standard'],

	'description': ['String', 'Standard'],	
	'pic_key': ['BlobKey', 'Standard'],
	'pic_url': ['String', 'Standard'],
	
	'size': ['Integer', 'Radio'],
	'timer': ['Integer', 'Standard'],
	'event_date': ['DateTime', 'Standard'],

	'status': ['String', 'Select'],
	'is_realized': ['Boolean', 'Checkbox'],
	'needs_mtnc': ['Boolean', 'Checkbox'],
	
	'is_active': ['Boolean', 'Checkbox'], 
	'is_critical': ['Boolean', 'Checkbox'],
	'is_private': ['Boolean', 'Checkbox'],
	'at_anytime': ['Boolean', 'Checkbox'], 

	'comments': ['Text', 'Standard'],
	'tag': ['String', 'Standard'],
	
	'details': ['Json', ''] ,
	
	'best_time': ['Details', 'Standard'],
	'trigger': ['Details', 'Standard'], 
	'exceptions': ['Details', 'Standard'],
	
	'repeats': ['Details', 'Select'], 
	'every_x_days': ['Details', 'Standard'],
	'on_the_day': ['Details', 'Select'], 
	'of_month': ['Details', 'Select'],

	'every_mon': ['Details', 'Checkbox'],
	'every_tue': ['Details', 'Checkbox'], 
	'every_wed': ['Details', 'Checkbox'], 
	'every_thu': ['Details', 'Checkbox'], 
	'every_fri': ['Details', 'Checkbox'], 
	'every_sat': ['Details', 'Checkbox'], 
	'every_sun': ['Details', 'Checkbox'],

	'money_cost': ['Integer', 'Standard'],
	'cost_frequency': ['Details', 'Select'],
	'frequency': ['Details', 'Select'],
	'birthday': ['Details', 'Standard'],
	'source': ['Details', 'Standard'],
	'question': ['Details', 'Standard'],
	'chapter_duration': ['Details', 'Standard'],
}



ksu_type_attributes = {
	'Base': [
		'ksu_type', 
		'ksu_subtype', 
		'reason_id',
		
		'description', 
		# 'pic_key',
		'pic_url',

		'is_private',
		'comments',
		'tag',		
		'cost_frequency',			
	],

	'Action': [
		'money_cost',
		'best_time', 
		'trigger',
		'exceptions',
		
		'size',
		'timer',
		'event_date',

		'repeats',
		'every_x_days',
		'on_the_day', 
		'of_month',

		'every_mon',
		'every_tue', 
		'every_wed', 
		'every_thu', 
		'every_fri', 
		'every_sat', 
		'every_sun',
	
		'is_active', 
		'is_critical',
		'at_anytime',		
	],

	'Objective': [
		'money_cost',
		'event_date',
	],

	'LifePiece':[
		'money_cost',
		'status',
		'needs_mtnc',						
	],

	'Experience': [
		'frequency',
		'event_date',
		'chapter_duration',
	], 

	'Contribution': [], 

	'SelfAttribute': [], 

	'Person': [
		'frequency',
		'birthday',
	],

	'Situation': [], 

	'Possesion': [], 

	'Wisdom': ['source'], #Meter attributo para indicar si es self knowledge o general knowledge

	'Indicator': [
		'question',
		'frequency',
		'event_date',
	]
}

