$('#ksu_type').on('change',function(){
	if (this.value != 'Gene'){
		$('#assignedKSU').removeClass('hidden');
	} else {
		$('#assignedKSU').addClass('hidden');
	}

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


	d_EditorTitle = {
		'Gene': 'KASware Standard Unit Editor',
		'KeyA': 'Key Action Editor',
		// 'MinO': 'Mini Objective Editor',
		'BigO': 'Objective Editor',
		'Drea': 'Dream Editor',
		'Wish': 'Wish Editor',
		'Prin': 'Principle Editor',
		'EVPo': 'End Value Editor',
		'ImPe': 'Important People Editor',
		'RTBG': 'Reason To Be Grateful Editor',
		'Idea': 'Wise Idea Editor',
		'NoAR': 'Reminder Editor',
		'MoRe': 'Money Requirement Editor',
		'ImIn': 'Indicator Editor'
	}

	$('#KsuEditorTitle').text(d_EditorTitle[this.value]);

});


$('input[type=radio][name=ksu_subtype]').on('change',function(){
	if (this.value != 'KAS1or2'){
		$('#KeyA_KAS1or2').addClass('hidden');
	} else {
		$('#KeyA_KAS1or2').removeClass('hidden');
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
		} else {
			$('#repeats_on').addClass('hidden');
		}
		$('#repeats_every_footnote').text(d_repeats_legend[this.value]);
	} else {
		$('#repeatsDetails').addClass('hidden');
	}

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
