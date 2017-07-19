
ksu_types = {
		
	#Life Pieces
	'JoyGenerator':[#What do you want to be doing? 
		'JoyGenerator' #If the parent is other joy generator, then its a generator instance: E.g. Estar jugando el juego de aventura en turno >> #E.g. Estar jugando Zelda breath of the wild
	]
	
	'Self':[#Who is the best person you could be?
		'Mind', #Knowledge and skills
		'Soul', #'Attitude', #Connciousness and inner peace
		'Body', #PhisicalAttribute, Health and vitality
		'Achievement', #Personal achievement
	],

	'Person':[ #Who you want in your life 'Love', #Important People. Love & Friendship
		'Person', #If the parent is another person, then the parent is a group of people #'Group',		
	],

	'Possesion':[ #What you want to have
		'Stuff', #For personal use
		'Status', #Aqui entrarían los trabajos o cualquier asset que viva en las mentes de otras personas.
		'MoneyOrAsset', #Dinero o assets tangibles
	]	

	'Surroundings':[#What are the characteristics of the place where you want to live, #Environment & Stuff. Stuff & Other order and peace
		'PersonalSpace', #The wording needs work
		'CollectiveSpace',
	],

	'GreaterGood':[ #Whats the impact you want to have in others peoples life and the envieronment?
		'Social',
		'Environment',
	],

	#Actions	
	'Action': [
		'Proactive',
		'Reactive',
		'Negative'
	],	

	'Objective': [ #Group actions or other milestones
		'Objective', #If the parent is another objective then its a milestone#'Milestone',
	],

	
	'Idea':[ #Your personal constitution. Non actionable knowledge that you believe should guide your behaviour.
		'Idea', #If the idea has a parent then is not a principle. BRILIANT! #'Principle', #Sirve para organizar y auditar
	], 

	#Indicator Results The concreate metrics you pick to measure success
	'UserIndicator': [
		'RealitySnapshot',
		'BinaryPerception',
		'TernaryPerception',
	],

}

event_types = {
	'EndValue', #Generado por Joy Generatos 
	'WishRealized',# Generado por Life Pieces al cambiar de status
	'Progress', #Generado por objetivos
	'Effort', #Generado por acciones al ser ejecutadas
	'Measurement' #Generaddo por indicadores
}