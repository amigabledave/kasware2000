

ksu_set  = [
	{'ksu_id':'ksu_01', 'reason_id': None},
	{'ksu_id':'ksu_02', 'reason_id': 'ksu_01'},
	{'ksu_id':'ksu_03', 'reason_id': 'ksu_06'},
	{'ksu_id':'ksu_04', 'reason_id': 'ksu_01'},
	{'ksu_id':'ksu_05', 'reason_id': None},
	{'ksu_id':'ksu_06', 'reason_id': 'ksu_04'},
]

superficial_scores = {
	'ksu_01':{'merits':5, 'events':2, 'minutes':1},
	'ksu_02':{'merits':5, 'events':2, 'minutes':1},
	'ksu_03':{'merits':5, 'events':2, 'minutes':1},
	'ksu_04':{'merits':5, 'events':2, 'minutes':1},
	'ksu_05':{'merits':5, 'events':2, 'minutes':1},
	'ksu_06':{'merits':5, 'events':2, 'minutes':1},
}

generations = 2

def calculate_deep_scores(ksu_set, superficial_scores, generations):

	parent_ksus = []
	parent_childs = {}
	deep_scores = {}

	for ksu in ksu_set:
		
		ksu_id = ksu['ksu_id']
		reason_id = ksu['reason_id'] 
		
		if reason_id:
			if reason_id not in parent_ksus:
				deep_scores[reason_id] = {'merits':0, 'events':0, 'minutes':0}
				parent_ksus.append(reason_id)
				parent_childs[reason_id] = [ksu_id]
			
			elif ksu_id not in parent_childs[reason_id]:
				parent_childs[reason_id].append(ksu_id)

	print
	print parent_ksus
	print parent_childs
	print

	for i in range(generations):
		for ksu in parent_ksus:
			new_childs = [] + parent_childs[ksu]
			for child in parent_childs[ksu]:
				if child in parent_childs:
					for grand_child in parent_childs[child]: 
						if grand_child not in new_childs:
							new_childs.append(grand_child)
			parent_childs[ksu] = new_childs

	print parent_ksus
	print parent_childs
	print

	for ksu in parent_ksus:
		score_types = ['merits', 'events', 'minutes']

		for score_type in score_types:
			deep_scores[ksu][score_type] += superficial_scores[ksu][score_type]

		for child in parent_childs[ksu]:
			for score_type in score_types:
				deep_scores[ksu][score_type] += superficial_scores[child][score_type]

	z = superficial_scores.copy()
	z.update(deep_scores)

	return z

print
print calculate_deep_scores(ksu_set, superficial_scores, generations)

