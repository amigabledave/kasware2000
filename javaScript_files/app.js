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
		if ($('#ksu_id').val() == ''){
			$('#KAS1').prop("checked", true);
			$('#KeyA_KAS1').removeClass('hidden');
		}

	} else {
		$('#KeyA').addClass('hidden');
	}	

	if (this.value == 'OTOA'){
		$('#OTOA').removeClass('hidden');
	} else {
		$('#OTOA').addClass('hidden');
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
});


$('input[type=radio][name=ksu_subtype]').on('change',function(){
	

	if (this.value == 'KAS1'){
		$('#KeyA_KAS1').removeClass('hidden');
	} else {
		$('#KeyA_KAS1').addClass('hidden');
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
	console.log('Se detecto el cambio de KSU_SUBTYPE');
	console.log(this.value);
	$('#NewKSU').attr("ksusubtype", this.value);
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



$(document).on('change', '.KsuEditor_Repeats', function(){

	var ksu = $(this).closest('#MissionKSU');

	d_repeats_legend = {
	'R001':'Days',
	'R007':'Weeks',
	'R030':'Months',
	'R365':'Years'};

	if (this.value != 'R000') {
		ksu.find('#repeatsDetails').removeClass('hidden');
		if (this.value == 'R007'){
			ksu.find('#repeats_on').removeClass('hidden');
			ksu.find('#repeats_every').addClass('hidden');
		} else {
			ksu.find('#repeats_on').addClass('hidden');
			ksu.find('#repeats_every').removeClass('hidden');
		}
		ksu.find('#repeats_every_footnote').text(d_repeats_legend[this.value]);
	} else {
		ksu.find('#repeatsDetails').addClass('hidden');
	}
});


// $('.UserActionButton').on('click', function(){
$(document).on('click', '.UserActionButton', function(){
	console.log('Si esta detectando que se aprieta el boton');
	var ksu = $(this).closest('#MissionKSU');
	var ksu_id = ksu.attr("value");
	var user_action = $(this).attr("value");
	var kpts_value = ksu.find('#kpts_value option:selected').val();
	var event_comments = ksu.find('#event_comments').val()

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


	if (user_action == 'ReactiveMissionDone'){
		user_action = 'MissionDone'};


	if (user_action == 'MissionRecordValue' || user_action == 'ViewerRecordValue'){
		user_action = 'RecordValue'
		kpts_value = ksu.find('#select_indicator_value option:selected').val()
		
		if(kpts_value == undefined){
			kpts_value = ksu.find('#open_indicator_value').val()};	
		};

	if(kpts_value == undefined){
		kpts_value = 0};

	if(event_comments == undefined){
		event_comments = ''};

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


$('.SaveNewKSUButton').on('click', function(){
	var ksu = $(this).closest('#NewKSU');
	var ksu_type = ksu.attr("ksutype");
	var ksu_subtype = ksu.attr("ksusubtype");

	var description = ksu.find('#description').val();
	var secondary_description = ksu.find('#secondary_description').val();
	var next_event = ksu.find('#next_event').val();
	var best_time = ksu.find('#best_time').val();
	var kpts_value = ksu.find('#kpts_value option:selected').val();

	var importance = ksu.find('#importance').val();
	var tags = ksu.find('#tags_value').val();
	var comments = ksu.find('#comments').val();

	var frequency = ksu.find('#frequency').val();
	var repeats = ksu.find('#repeats').val();		

	var is_active = ksu.find('#is_active').is(':checked');
	var is_critical = ksu.find('#is_critical').is(':checked');
	var is_private = ksu.find('#is_private').is(':checked');
	
	var repeats_on_Mon = ksu.find('#repeats_on_Mon').is(':checked');
	var repeats_on_Tue = ksu.find('#repeats_on_Tue').is(':checked'); 
	var repeats_on_Wed = ksu.find('#repeats_on_Wed').is(':checked'); 
	var repeats_on_Thu = ksu.find('#repeats_on_Thu').is(':checked');
	var repeats_on_Fri = ksu.find('#repeats_on_Fri').is(':checked');
	var repeats_on_Sat = ksu.find('#repeats_on_Sat').is(':checked');
	var repeats_on_Sun = ksu.find('#repeats_on_Sun').is(':checked');

	var money_cost = ksu.find('#money_cost').val();
	var birthday = ksu.find('#birthday').val();

	
	if (description == ''){
		description = ksu.find('#description').text();
		secondary_description = ksu.find('#secondary_description').text();
	};

	ksu.fadeOut("slow")
	
	$.ajax({
		type: "POST",
		url: "/EventHandler",
		dataType: 'json',
		data: JSON.stringify({
			'user_action': 'SaveNewKSU',
			'ksu_type': ksu_type,
			'ksu_subtype': ksu_subtype,
			
			'description':description,
			'secondary_description':secondary_description,
			'next_event':next_event,
			'best_time':best_time,
			'kpts_value': kpts_value,

			'importance':importance,
			'tags':tags,
			'comments':comments, 
		
			'is_active':is_active,
			'is_critical':is_critical, 
			'is_private':is_private,

			'frequency':frequency,
			'repeats':repeats,
	
			'repeats_on_Mon':repeats_on_Mon,
			'repeats_on_Tue':repeats_on_Tue,
			'repeats_on_Wed':repeats_on_Wed,
			'repeats_on_Thu':repeats_on_Thu,
			'repeats_on_Fri':repeats_on_Fri,
			'repeats_on_Sat':repeats_on_Sat,
			'repeats_on_Sun':repeats_on_Sun,

			'money_cost':money_cost,

		})
	})
	.done(function(data){
		console.log(data);
		ksu.find('#description').val('');
		ksu.find('#secondary_description').val('');
		ksu.find('#best_time').val('');
		ksu.find('#next_event').val('');
		ksu.find('#tags_value').val('');
		ksu.find('#importance').val(2);
		ksu.find('#kpts_value').val(0.25);
		ksu.find('#is_critical').prop('checked', false);
		ksu.find('#is_active').prop('checked', true);
		ksu.find('#money_cost').val('');

		if (ksu_subtype == ''){
			ksu_subtype = ksu_type
		};

		console.log('Este es el tipo de KSU que ando pidiendo guardar:');
		console.log(ksu_type);
		console.log(ksu_subtype);

		var Templates = {
			'KeyA': $('#NewKSUTemplate_KeyA').clone(),
			'KAS1': $('#NewKSUTemplate_KAS1').clone(),
			'KAS3': $('#NewKSUTemplate_KAS3').clone(),
			'KAS4': $('#NewKSUTemplate_KAS4').clone(),
			
			'Obje': $('#NewKSUTemplate_Obje').clone(),
			'BigO': $('#NewKSUTemplate_BigO').clone(),
			'Wish': $('#NewKSUTemplate_Wish').clone(),
			'Dream': $('#NewKSUTemplate_Dream').clone()
		}


		var new_ksu = Templates[ksu_subtype];

		new_ksu.attr("id", "MissionKSU");
		new_ksu.attr("value",data['ksu_id']);
		new_ksu.find('#ksu_id').attr("value",data['ksu_id']);

		new_ksu.find('#description').val(description);
		new_ksu.find('#secondary_description').val(secondary_description);
		new_ksu.find('#kpts_value').val(kpts_value);
		new_ksu.find('#best_time').val(best_time);
		new_ksu.find('#next_event').val(next_event);

		new_ksu.find('#importance').val(importance);
		new_ksu.find('#tags').val(tags);
		new_ksu.find('#ksu_subtype').text(ksu_subtype);

		new_ksu.find('#is_critical').prop('checked', is_critical);
		new_ksu.find('#is_active').prop('checked', is_active);
		new_ksu.find('#is_private').prop('checked', is_private);

		new_ksu.find('#money_cost').val(money_cost);

		new_ksu.removeClass('hidden');
		new_ksu.prependTo('#NewKSUsHolder');
		new_ksu.fadeIn("slow");

		if(is_critical && is_active){
			new_ksu.find('#description').css('color', 'red');				
		} else if (is_active){
			new_ksu.find('#description').css('color', 'black');				
		} else {
			new_ksu.find('#description').css('color', '#D3D3D3');
		};

		ksu.fadeIn("slow");		
	});
});


$('.DeleteEventButton').on('click', function(){
	var event = $(this).closest('#ViewerEvent');
	var event_id = event.attr("value");
		
	event.fadeOut("slow")
	
	$.ajax({
		type: "POST",
		url: "/EventHandler",
		dataType: 'json',
		data: JSON.stringify({
			'user_action': 'DeleteEvent',
			'event_id': event_id,
		})
	})
	.done(function(data){
		console.log(data);

		var PointsToGoal = data['PointsToGoal'];

		if ( PointsToGoal <= 0){
			PointsToGoal = 'Achieved!'
		}; 
	
		$('#PointsToGoal').text(' ' + PointsToGoal);
		$('#EffortReserve').text(' ' + data['EffortReserve']);
		$('#Streak').text(' ' + data['Streak']);
	
	});
});


// $('.ShowDetailViewerButton').on('click', function(){
$(document).on('click', '.ShowDetailViewerButton', function(){

	var ksu = $(this).closest('#MissionKSU');
	
	var ScoreDetail = ksu.find('#ScoreDetail');
	ScoreDetail.toggleClass('hidden');

	var GlaphiconDiv = ksu.find('#PlusMinusGlyphicon');
	GlaphiconDiv.toggleClass('glyphicon-minus');
	GlaphiconDiv.toggleClass('glyphicon-plus');	
});


// $('.QuickAttributeUpdate').on('focusout', function(){
$(document).on('focusout', '.QuickAttributeUpdate', function(){
	var attr_key = $(this).attr("name");
	var attr_type = $(this).attr("type");
	var attr_value = $(this).val();
	if( attr_type == 'checkbox'){
		attr_value = $(this).is(':checked');
	};

	var ksu = $(this).closest('#MissionKSU');
	var ksu_id = ksu.attr("value");

	console.log(attr_key);
	console.log(attr_value);

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

		if( attr_type == 'checkbox'){
			var description = ksu.find('#description');
			var secondary_description = ksu.find('#secondary_description');
			var is_critical = ksu.find('#is_critical').is(':checked');
			var is_active = ksu.find('#is_active').is(':checked');
			console.log(is_active, is_critical);
			if(is_critical && is_active){
				description.css('color', 'red');				
			} else if (is_active){
				description.css('color', 'black');				
			} else {
				description.css('color', '#D3D3D3');
			};
		};

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


// Hace que se resize las cajas de texto con autoexpand
$(document)
    .one('focus.textarea', '.autoExpand', function(){
        var savedValue = this.value;
        this.value = '';
        this.baseScrollHeight = this.scrollHeight;
        this.value = savedValue;
    })
    .on('input.textarea', '.autoExpand', function(){
        var minRows = this.getAttribute('data-min-rows')|0,
            rows;
        this.rows = minRows;
        rows = Math.ceil((this.scrollHeight - this.baseScrollHeight) / 16);
        this.rows = minRows + rows;
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
