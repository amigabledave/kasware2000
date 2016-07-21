var userCategories = {
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


$('#ksu_type').on('change',function(){

	if (this.value == 'KeyA'){
		$('#KeyA').removeClass('hidden');
	} else {
		$('#KeyA').addClass('hidden');
	}	

	if (this.value == 'BigO'){
		$('#BigO').removeClass('hidden');
	} else {
		$('#BigO').addClass('hidden');
	}

	if (this.value == 'Wish'){
		$('#Wish').removeClass('hidden');
	} else {
		$('#Wish').addClass('hidden');
	}

	if (this.value == 'EVPo'){
		$('#EVPo').removeClass('hidden');
	} else {
		$('#EVPo').addClass('hidden');
	}

	if (this.value == 'Idea'){
		$('#Idea').removeClass('hidden');
	} else {
		$('#Idea').addClass('hidden');
	}

	if (this.value == 'ImPe'){
		$('#ImPe').removeClass('hidden');
	} else {
		$('#ImPe').addClass('hidden');
	}

	if (this.value == 'RTBG'){
		$('#RTBG').removeClass('hidden');
	} else {
		$('#RTBG').addClass('hidden');
	}

	if (this.value == 'ImIn'){
		$('#ImIn').removeClass('hidden');
	} else {
		$('#ImIn').addClass('hidden');
	}

	d_EditorTitle = {
		'Gene': 'KASware Standard Unit Editor',
		'KeyA': 'Key Action Editor',
		// 'MinO': 'Mini Objective Editor',
		'BigO': 'Objective Editor',
		'Drea': 'Dream Editor',
		'Wish': 'Wish Editor',
		// 'Prin': 'Principle Editor',
		'EVPo': 'End Value Editor',
		'ImPe': 'Important Person Editor',
		'RTBG': 'Reason To Be Grateful Editor',
		'Idea': 'Wise Idea Editor',
		'NoAR': 'Reminder Editor',
		'MoRe': 'Money Requirement Editor',
		'ImIn': 'Indicator Editor'
	}

	$('#KsuEditorTitle').text(d_EditorTitle[this.value]);

	var new_catDropdown = '<select class="form-control" name="local_category" id="local_category">';	
	local_categories = userCategories[this.value];
	for( c in local_categories){
		new_catDropdown = new_catDropdown + '<option value="' + local_categories[c] + '">' + local_categories[c] + '</option>'
	}
	new_catDropdown = new_catDropdown + '</select>'
	$('#local_category').replaceWith(new_catDropdown);
});


$('input[type=radio][name=ksu_subtype]').on('change',function(){
	

	if (this.value == 'KAS1or2'){
		$('#KeyA_KAS1or2').removeClass('hidden');
		$('#KeyA_KAS1or2or3').removeClass('hidden');
	} else {
		$('#KeyA_KAS1or2').addClass('hidden');
	}

	if (this.value == 'KAS3'){
		$('#KeyA_KAS3').removeClass('hidden');
		$('#KeyA_KAS1or2or3').removeClass('hidden');
	} else {
		$('#KeyA_KAS3').addClass('hidden');	
	}

	if (this.value == 'KAS4'){
		$('#KeyA_KAS4').removeClass('hidden');
		$('#KeyA_KAS1or2or3').addClass('hidden');		
	} else {
		$('#KeyA_KAS4').addClass('hidden');
		
	}
});


$('#repeats').on('change',function(){

	d_repeats_legend = {
	'R001':'Days',
	'R007':'Weeks',
	'R030':'Months',
	'R365':'Years'};

	if (this.value != 'R000') {
		$('#repeatsDetails').removeClass('hidden');
		if (this.value == 'R007'){
			$('#repeats_on').removeClass('hidden');
			$('#repeats_every').addClass('hidden');
		} else {
			$('#repeats_on').addClass('hidden');
			$('#repeats_every').removeClass('hidden');
		}
		$('#repeats_every_footnote').text(d_repeats_legend[this.value]);
	} else {
		$('#repeatsDetails').addClass('hidden');
	}
});

$('.UserActionButton').on('click', function(){
	var ksu = $(this).closest('#MissionKSU');
	var ksu_id = ksu.attr("value");
	var user_action = $(this).attr("value");

	var kpts_reward = ksu.find('#kpts_reward option:selected').val();
	var kpts_punishment = ksu.find('#kpts_punishment option:selected').val();

	var mission_actions = ['MissionDone', 'MissionPush', 'MissionSkip' ,'MissionDelete']

	if ($.inArray(user_action, mission_actions)!= -1){
		ksu.animate({
			"opacity" : "0",
			},{
				"complete" : function() {
				ksu.remove();
				}
			})
		};

	$.ajax({
		type: "POST",
		url: "/EventHandler",
		dataType: 'json',
		data: JSON.stringify({
			'ksu_id': ksu_id,
			'user_action': user_action,
			'kpts_reward':kpts_reward,
			'kpts_punishment':kpts_punishment
		})
	})
	.done(function(data){
		var EventScore = data['EventScore'];
		var kpts_type = data['kpts_type'];
		var PointsToGoal = parseFloat($('#PointsToGoal').text())

		if (kpts_type == 'SmartEffort'){
			PointsToGoal -= EventScore;
		};

		if (kpts_type == 'Stupidity'){
			PointsToGoal += EventScore;
		};

		// var TotalScore = parseInt($('#TotalScore').text()) + EventScore;

		if (isNaN(PointsToGoal)){
			PointsToGoal = 0
		};

		if ( PointsToGoal <= 0){
			PointsToGoal = 'Achieved!'
		}; 
	
		$('#PointsToGoal').text(' ' + PointsToGoal);
		// $('#TotalScore').text(' ' + TotalScore); 
		// alert(data['mensaje']);

		var disapearing_suptypes = ['KAS2'];
		var ksu_subtype = data['ksu_subtype'];
		if ($.inArray(ksu_subtype, disapearing_suptypes)!= -1){
			ksu.animate({
				"opacity" : "0",
				},{
					"complete" : function() {
					ksu.remove();
					}
				})
			};

	});
});


$('.ShowDetailViewerButton').on('click', function(){
	var ScoreDetail = $(this).closest('#MissionKSU').find('#ScoreDetail');
	var GlaphiconDiv = $(this).closest('#MissionKSU').find('#ShowDetailButton').children();
	GlaphiconDiv.toggleClass('glyphicon-minus');
	GlaphiconDiv.toggleClass('glyphicon-plus');
	ScoreDetail.toggleClass('hidden');
});


$('.ShowDetailMissionButton').on('click', function(){
	var ScoreDetail = $(this).closest('#MissionKSU').find('#ScoreDetail');
	var GlaphiconDiv = $(this).children();
	GlaphiconDiv.toggleClass('glyphicon-minus');
	GlaphiconDiv.toggleClass('glyphicon-plus');
	ScoreDetail.toggleClass('hidden');
});


var updateKsuScore = function(x){	
	var ksu = $(x).closest('#MissionKSU');
	var kpts_reward = ksu.find('#kpts_reward').val();
	var score = ksu.find('#KsuKpts');	
	score.text(kpts_reward);
};

$('.kpts_reward').on('change', function(){
	updateKsuScore(this);
});




// function al_cargar(){
// 	console.log('mas o menos ahi va')
// };
// $(al_cargar);

// $('body').on('click', function(){
// 	console.log('Logre linkear un archivo de JS a KASware!!! :)')
// });

// $(document).ready(function(){
// 	$('body').on('click', function(){
// 		console.log('Logre linkear un archivo de JS a KASware!!! :)')
// 	});
// });
