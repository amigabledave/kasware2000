var userCategories = {
	'Gene': ['Unassigned'],
	'KeyA': ['Unassigned'],
	'Obje': ['Unassigned'],
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


$('.DummyInput').on('change',function(){
	
	var ksu_attr = $(this).attr("ksuattr");
 
	if (ksu_attr == 'kpts_value'){
		$('#kpts_value').val(this.value);
	};

	if (ksu_attr == 'next_event'){
		$('#next_event').val(this.value);
	};

	if (ksu_attr == 'frequency'){
		$('#frequency').val(this.value);
	};

	if (ksu_attr == 'secondary_description'){
		$('#secondary_description').val(this.value);
	};

	if (ksu_attr == 'birthday'){
		$('#birthday').val(this.value);
	};

	if (ksu_attr == 'best_time'){
		$('#best_time').val(this.value);
	};
});


$('#ksu_type').on('change',function(){

	if (this.value == 'KeyA'){
		$('#KeyA').removeClass('hidden');
		console.log('Una key action')
		if ($('#ksu_id').val() == ''){
			$('#KAS1or2').prop("checked", true);
			$('#KeyA_KAS1or2').removeClass('hidden');
		}

	} else {
		$('#KeyA').addClass('hidden');
	}	

	if (this.value == 'Obje'){
		$('#Obje').removeClass('hidden');
	} else {
		$('#Obje').addClass('hidden');
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
		'Obje': 'Objective Editor',
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
	} else {
		$('#KeyA_KAS1or2').addClass('hidden');
	}

	if (this.value == 'KAS3'){
		$('#KeyA_KAS3').removeClass('hidden');
	} else {
		$('#KeyA_KAS3').addClass('hidden');	
	}

	if (this.value == 'KAS4'){
		$('#KeyA_KAS4').removeClass('hidden');		
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

	var kpts_value = ksu.find('#kpts_value option:selected').val();

	var dissapear_before_done = ['MissionDone', 'MissionPush', 'MissionSkip' ,'MissionDelete', 'ViewerDelete','GraveyardDelete', 'GraveyardReanimate', 'MissionRecordValue']
	
	if ($.inArray(user_action, dissapear_before_done)!= -1){
		ksu.animate({
			"opacity" : "0",
			},{
				"complete" : function() {
				ksu.remove();
				}
			})
		};

	if (user_action == 'MissionRecordValue' || user_action == 'ViewerRecordValue'){
		event_comments = ksu.find('#event_comments').val()
		user_action = 'RecordValue'
		kpts_value = ksu.find('#select_indicator_value option:selected').val()
		
		if(kpts_value == undefined){
			kpts_value = ksu.find('#open_indicator_value').val()};
		
		if(kpts_value == undefined){
			kpts_value = 0};	
		};

	$.ajax({
		type: "POST",
		url: "/EventHandler",
		dataType: 'json',
		data: JSON.stringify({
			'ksu_id': ksu_id,
			'user_action': user_action,
			'kpts_value':kpts_value,
			'event_comments':event_comments
		})
	})
	.done(function(data){
		console.log(data);
		var EventScore = data['EventScore'];
		var kpts_type = data['kpts_type'];
		var PointsToGoal = data['PointsToGoal']

		if ( PointsToGoal <= 0){
			PointsToGoal = 'Achieved!'
		}; 
	
		$('#PointsToGoal').text(' ' + PointsToGoal);
		$('#EffortReserve').text(' ' + data['EffortReserve']);
		$('#Streak').text(' ' + data['Streak']);


		if ($.inArray(user_action, dissapear_before_done)!= -1){
			$('#MissionValue').text(parseFloat($('#MissionValue').text())-data['kpts_value']);
		};

		var ksu_subtype = data['ksu_subtype'];

		if (user_action == 'SendToMission' || user_action == 'ViewerDone' || user_action == 'RecordValue'){
			ksu.find('#pretty_next_event').text(data['pretty_next_event']);
		};

		if (user_action == 'ViewerOnOff'){
			console.log(data['is_active'])
			if (data['is_active']){
				ksu.find('#is_active').css({'color': 'black'});
				ksu.find('#ViewerOnOffButton').removeClass('btn-success');
				ksu.find('#ViewerOnOffButton').addClass('btn-warning');
			} else {
				ksu.find('#is_active').css({'color': '#D3D3D3'});
				ksu.find('#ViewerOnOffButton').removeClass('btn-warning');
				ksu.find('#ViewerOnOffButton').addClass('btn-success');				
			}

		};
		
		var dissapear_after_done_subtypes = ['KAS2', 'Wish', 'Dream', 'Obje', 'BigO'];
		var dissapear_after_done_actions = ['ViewerDone'];

		if (($.inArray(ksu_subtype, dissapear_after_done_subtypes)!= -1) && ($.inArray(user_action, dissapear_after_done_actions)!= -1)){
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
	var ksu = $(this).closest('#MissionKSU');
	
	var ScoreDetail = ksu.find('#ScoreDetail');
	ScoreDetail.toggleClass('hidden');

	var GlaphiconDiv = ksu.find('#PlusMinusGlyphicon');
	GlaphiconDiv.toggleClass('glyphicon-minus');
	GlaphiconDiv.toggleClass('glyphicon-plus');
	
});


var updateKsuScore = function(x){	
	var ksu = $(x).closest('#MissionKSU');
	var kpts_value = ksu.find('#kpts_value').val();
	var score = ksu.find('#KsuKpts');	
	score.text(kpts_value);
};

$('.kpts_value').on('change', function(){
	updateKsuScore(this);
});


$('.QuickAttributeUpdate').on('focusout', function(){
	var attr_key = $(this).attr("name");
	var attr_value = $(this).val();
	var ksu = $(this).closest('#MissionKSU');
	var ksu_id = ksu.attr("value");

	$.ajax({
		type: "POST",
		url: "/EventHandler",
		dataType: 'json',
		data: JSON.stringify({
			'ksu_id': ksu_id,
			'user_action': 'UpdateKsuAttribute',
			'attr_key':attr_key,
			'attr_value':attr_value,
		})
	})
	
	.done(function(data){
		console.log(data['updated_value']);

		if (attr_key == 'best_time'){
			ksu.find('#pretty_best_time').text(data['updated_value'])};

		if (attr_key == 'next_event'){
			ksu.find('#pretty_next_event').text(data['updated_value'])};

		if (attr_key == 'description'){
			ksu.find('#description').val(data['updated_value'])};
	})
});



// Hace que sea posible desseleccionar radios    
var allRadios = document.getElementsByName('ksu_subtype');
var booRadio;
var x = 0;
for(x = 0; x < allRadios.length; x++){

    allRadios[x].onclick = function() {
        if(booRadio == this){
            this.checked = false;
            booRadio = null;
        }else{
            booRadio = this;
        }
    };
}




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
