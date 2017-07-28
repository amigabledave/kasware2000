# Meter attributo nuevo en {MasterKSU.html:[], KASware3.py: [ksu_type_attributes, attributes_guide], KASware3app.js: [ksu_type_attributes, attributes_guide],}


ksu_types = [

	#Actions	
	[['Action', 'Action'], [
		['Proactive', 'Proactive'],
		['Reactive', 'Reactive'],
		['Negative', 'Negative']
	]],	

	[['Objective', 'Objective'], [ #Group actions or other milestones
		['Objective', 'Objective'], #If the parent is another objective then its a milestone#'Milestone',
	]],
	
	[['Wisdom', 'Wisdome'], [#Idea #Your personal constitution. Non actionable knowledge that you believe should guide your behaviour.
		['Idea', 'Idea'], #If the idea has a parent then is not a principle. BRILIANT!
		['Principle', 'Principle'], #Sirve para organizar y auditar
	]], 
		
	#Life Pieces
	[['JoyGenerator', 'Joy Generator'], [#What do you want to be doing? #'Surroundings = Aqui entra estar viviendo en Canada
		['Moment', 'Moment'], #Whaterver < Nice < Memorable < Epic < Legendary
		['JoyMine', 'Joy Mine'], #Algo concreto que genera momentos del mismo tipo... E.g. Estar jugando Zelda breath of the wild
		['Chapter', 'Chapter'], #Agrupa varios momentos, pero no es un momento en si por lo que no tiene importancia. El padre puede ser otro chapter .E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild
		#'JoyGenerator' #If the parent is other joy generator, then its a generator instance: E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild	
	]],

	[['Purpose', 'Purpose'], [ #Whats the impact you want to have in others peoples life and the envieronment? Antes Meaning GreaterGood
		['Purpose', 'Purpose'] #  #Personal achievement. Antes estaba en self 'GreaterGood', #'Social', 'Environment',		
	]],
	
	[['SelfAttribute', 'Attribute'], [# Antes Self. #Who is the best person you could be? 'Antes tenia Achievemnt pero ahora queda en meaning',
		['Attitude', 'Attitude'], #'SoulSkill', #Connciousness and inner peace
		['KnowledgeOrSkill', 'Skill or Knowledge'], #MindSkill Knowledge and skills		
		['BodyFeature', 'Body Feature'], #PhisicalAttribute, Health and vitality
	]],

	[['Person', 'Person'], [ #Who you want in your life 'Love', #Important People. Love & Friendship
		['Individual', 'Individual'], #Person #If the parent is another person, then the parent is a group of people #'Group',
		['Group', 'Group'],
	]],

	[['Possesion', 'Possesion'], [ #What you want to have
		['Stuff', 'Stuff'], #For personal use
		['Status', 'Status'], #Aqui entrarian los trabajos o cualquier asset que viva en las mentes de otras personas.
		['Asset', 'Asset'], #Dinero o assets tangibles. MoneyOrAsset
		['Order', 'Order'], #No estoy seguro si la voy a dejar o no. "Clean room, email inbox... etc"
	]],	


	#Indicator Results The concreate metrics you pick to measure success
	[['UserIndicator', 'Indicator'], [
		['RealitySnapshot', 'Reality'],
		['BinaryPerception', 'Perception'],
		# ['TernaryPerception', ],
	]],
]


event_types = {
	'EndValue', #Generado por Joy Generatos 
	'Proof', # Generado Being, Purpose, Idea... (ejemplos de tu siendo la persona que quieres ser) #Necesita pulirse
	'WishRealized',# Generado por Life Pieces al cambiar de status
	'Progress', #Generado por objetivos
	'Effort', #Generado por acciones al ser ejecutadas
	'Measurement', #Generaddo por indicadores
}


ksu_type_attributes = {
	'Base': [
		'ksu_type', 
		'ksu_subtype', 
		'reason_id',
		
		'description', 
		'pic_key',
			
		'is_realized',
		'needs_mtnc',

		'is_active', 
		'is_critical',
		'is_private',
		'at_anytime', 

		'is_visible', 		 
		'in_graveyard',

		'comments',
		'tag',
	],

	'Action': [
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
	],

	'Objective': [],
	
	'Wisdom': [], 

	'JoyGenerator': [], 

	'Purpose': [], 

	'SelfAttribute': [], 

	'Person': [], 

	'Possesion': [], 

	'UserIndicator': []
}


attributes_guide = {
	'theory_id': 'Key', 	
	'created': 'DateTime', 
	'ksu_type': 'String', 
	'ksu_subtype': 'String',
	'reason_id': 'Key',

	'description': 'String',	
	'pic_key': 'BlobKey',
	'pic_url': 'String',
	
	'size': 'Integer',
	'timer': 'Integer',
	'event_date': 'DateTime',

	'is_realized': 'Boolean',
	'needs_mtnc': 'Boolean',
	
	'is_active': 'Boolean', 
	'is_critical': 'Boolean',
	'is_private': 'Boolean',
	'at_anytime': 'Boolean', 

	'is_visible': 'Boolean',  
	'in_graveyard': 'Boolean',

	'comments': 'Text',
	'tag': 'String',
	
	'details': 'Json' ,
	
	'best_time': 'Details',
	'trigger': 'Details', 
	'exceptions': 'Details',
	
	'repeats': 'Details', 
	'every_x_days': 'Details',
	'on_the_day': 'Details', 
	'of_month': 'Details',

	'every_mon': 'Details',
	'every_tue': 'Details', 
	'every_wed': 'Details', 
	'every_thu': 'Details', 
	'every_fri': 'Details', 
	'every_sat': 'Details', 
	'every_sun': 'Details',
} 