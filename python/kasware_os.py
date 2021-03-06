os_ksus = [
	
	{'description':'Define/review your mission for today -- What would you have to do today to consider the day a success?',
	 'ksu_type':'KeyA', 
	 'ksu_subtype':'KAS1',
	 'kpts_value':1, 
	 'frequency':1,
	 'mission_view':'KickOff',
	 'is_active':True,
	 'is_critical':True,
	 'repeats':'R001',
	 'comments':'Suggestion: Add at least one Joy Generator! :)'},

	{'description':'Life excitement',
	 'secondary_description':"Did I wake up feeling excited?",
	 'ksu_type':'ImIn', 
	 'ksu_subtype':'BinaryPerception', 
	 'mission_view':'KickOff',
	 'mission_importance':2,
	 'is_active':True,
	 'frequency':1},

	{'description':'Life harmony',
	 'secondary_description':"Do you feel in harmony towards the life you live?",
	 'ksu_type':'ImIn', 
	 'ksu_subtype':'BinaryPerception', 
	 'mission_view':'KickOff',
	 'mission_importance':1,
	 'is_active':True,
	 'frequency':13},

	{'description':'Life fatigue',
	 'secondary_description':"Did I wake up feeling tire or sick?",
	 'ksu_type':'ImIn', 
	 'ksu_subtype':'BinaryPerception', 
	 'mission_view':'KickOff',
	 'mission_importance':3,
	 'is_active':True,
	 'frequency':1},

	{'description':'Life enjoyment',
	 'secondary_description':"How much did I enjoyed this day?",
	 'ksu_type':'ImIn', 
	 'ksu_subtype':'TernaryPerception',
	 'mission_view':'WrapUp',
	 'mission_importance':1,
	 'is_active':True, 
	 'frequency':1},

	{'description':'Life stress',
	 'secondary_description':"Did I feel significantly stressed during some moment today?",
	 'ksu_type':'ImIn', 
	 'ksu_subtype':'BinaryPerception', 
	 'mission_view':'WrapUp',
	 'mission_importance':2,
	 'is_active':True,
	 'frequency':1},

	{'description':'Oportunities for improvement',
	 'secondary_description':"Is there anything I would like to have done differently today?",
	 'ksu_type':'Diary',
	 'ksu_subtype':'Diary',
	 'mission_view':'WrapUp',
	 'is_active':True,
	 'mission_importance':5, 
	 'frequency':1},

	{'description':'Reasons to be proud',
	 'secondary_description':"Did I do anything today that I'm particularty proud off?",
	 'ksu_type':'Diary',
	 'ksu_subtype':'Diary',
	 'mission_view':'WrapUp',	 
	 'is_active':True,
	 'mission_importance':4, 
	 'frequency':1},

	{'description':'Awesome moments',
	 'secondary_description':"Did you experienced any awesome moment today?",
	 'ksu_type':'Diary',
	 'ksu_subtype':'Diary',
	 'mission_view':'WrapUp',
	 'mission_importance':3,
	 'is_active':True, 
	 'frequency':1}

]