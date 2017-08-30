# Meter attributo nuevo en {MasterKSU.html:[], KASware3.py: [ksu_type_attributes, attributes_guide], KASware3app.js: [ksu_type_attributes, attributes_guide],}


ksu_types = [

	#Actions	
	[['Action', 'Action'], [
		['Proactive', 'Proactive', True],
		['Reactive', 'Reactive', ''],
		['Negative', 'Negative', '']
	]],	

	[['Objective', 'Mile Stone'], [ #Group actions in a well define purpose
		['MiniObjective', 'Mini Objective', True], #If the parent is another objective then its a milestone#'Milestone',
		['BigObjective', 'Big Objective', ''], #If the parent is another objective then its a milestone#'Milestone',
	]],
	
	#Life Pieces
	[['Experience', 'Experience'], [#What do you want to be doing? #'Surroundings = Aqui entra estar viviendo en Canada
		['Moment', 'Moment', True], # Whaterver < Nice < Very nice < Memorable < Epic < Legendary		
		['JoyMine', 'Joy Mine', ''], #Algo concreto que genera momentos del mismo tipo... E.g. Estar jugando Zelda breath of the wild
		['Chapter', 'Chapter', ''], #Agrupa varios momentos, pero no es un momento en si por lo que no tiene importancia. El padre puede ser otro chapter .E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild		
	]],

	[['Contribution', 'Contribution'], [ #Whats the impact you want to have in others peoples life and the envieronment? Antes Meaning GreaterGood
		['StarFish', 'Star Fish', True], # Cada Star Fish matters, son contribuciones targeteadas para mejorar la vida de una persona
		['Calling', 'Calling', ''], # Aqui entran el trabajo que harias aunque no te pagaran	
		['WorldChange', 'World Change', ' '] #Aqui entran cualquier aspiraciones de cambiar el status del mundo mas alla de la vida de algunos individuos en particular
	]],
	
	[['SelfAttribute', 'Attribute'], [# Antes Self. #Who is the best person you could be? 'Antes tenia Achievemnt pero ahora queda en meaning',
		['Attitude', 'Attitude', ''], #'SoulSkill', #Connciousness and inner peace
		['KnowledgeOrSkill', 'Skill or Knowledge', True], #MindSkill Knowledge and skills		
		['BodyFeature', 'Body Feature', ''], #PhisicalAttribute, Health and vitality
		['Achievement', 'Achievement', ''] #Personal achievement.
	]],

	[['Person', 'Person'], [ #Who you want in your life 'Love', #Important People. Love & Friendship
		['Individual', 'Individual', True], #Person #If the parent is another person, then the parent is a group of people #'Group',
		['Group', 'Group', ''],
		['Role', 'Role'], #E.g. Sexual Partner, Someone to Play Magic, Etc... El padre solo puede ser una persona y puede tener varios padres
	]],

	[['Possesion', 'Possesion'], [ #What you want to have
		['Thing', 'Thing', True], #For personal use 	
		['Service', 'Service Access'], #For personal use
		['Asset', 'Asset', ''], #Dinero o assets tangibles. MoneyOrAsset
		['Job', 'Job', ''], #Aqui entran los trabajos que no harias si no te pagaran
	]],	

	[['Environment', 'Environment'], [ #Surrondings... Quiero de alguna forma indicar que se trata de los lugares donde pasas tiempo...
		['Private', 'Private', True],
		['Public', 'Public', ''], #Aqui entran los paises donde quieres vivir u otros lugares donde te gustaria pasar buena parte de tu tiempo
		['Order', 'Order', ''], #Algun attributo particular del lugar en cuestion 		
		#Tambien entra orden aqui. e.g. "Tener un cuarto ordenado"
	]],

	#Other	
	[['Wisdom', 'Wisdom'], [#Idea #Your personal constitution. Non actionable knowledge that you believe should guide your behaviour.
		['Principle', 'Principle', ''], #Sirve para organizar y auditar
		['Idea', 'Idea', True], #If the idea has a parent then is not a principle. BRILIANT!		
		['Learning', 'Learning', '']
	]], 

	[['Indicator', 'Indicator'], [#A concreate metrics you pick to measure success
		['Reality', 'Reality', ''],
		['Perception', 'Perception', True],
	]],
]


event_types = [	
	'EndValue', #Generado por momentos de Joy Generatos
	
	'Effort', #Generado por acciones al ser ejecutadas
	'Stupidity', #Generado por acciones al ser ejecutadas
	
	'Progress', #Generado por objetivos
	
	'WishRealized', #Generado por Life Pieces al cambiar de status
	'LifePieceGone', #Generado por Life Pieces al cambiar de status

	'PerceptionSnapshot', #Generaddo por indicadores de percepcion
	'RealitySnapshot',
]


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

	'needs_mtnc': ['Boolean', 'Checkbox'],
	'is_private': ['Boolean', 'Checkbox'],
	'anywhere': ['Boolean', 'Checkbox'], 
	'is_optional': ['Boolean', 'Checkbox'],

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

	'monitor': ['Boolean', 'Checkbox'],
	'goal_merits': ['Details', 'Standard'],
	'goal_events': ['Details', 'Standard'],
	'goal_minutes': ['Details', 'Standard'],
	'goal_time_frame': ['Details', 'Select'],

	'experience_quality':['Integer', 'Radio'],
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

		'monitor',				
		'goal_merits',
		'goal_events',
		'goal_minutes',
		'goal_time_frame'
	],

	'Action': [
		'money_cost',
		'cost_frequency',
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
	
		'anywhere',
		'status',
	],

	'Objective': [
		'money_cost',
		'cost_frequency',
		'event_date',
		'status',
	],

	'LifePiece':[
		'size',
		'money_cost',
		'cost_frequency',
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

	'Environment':[],

	'Possesion': [], 

	'Wisdom': ['source'], #Meter attributo para indicar si es self knowledge o general knowledge

	'Indicator': [
		'question',
		'frequency',
		'event_date',
	]
}



dashboard_template = {

	'EndValue':{
		'Score':0,
		'Legendary':[0,[]], #Event_id inside the []
		'Epic':[0,[]],
		'Memorable':[0,[]],
		'Nice':[0,[]],
		'Disappointing':[0,[]],
	}, 

	'KSU':{
		'ksu_id':['NumberOfEvents', 'TotalScore', ['Events_ids'], ['Childs']],
	},

	'Effort':{}, #Generado por acciones al ser ejecutadas
	
	'Stupidity':{}, #Generado por acciones al ser ejecutadas	
	
	'Progress':{}, #Generado por objetivos
	
	'WishRealized':{},# Generado por Life Pieces al cambiar de status 	

	'Measurement':{}, #Generaddo por indicadores
}
