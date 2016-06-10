$('#value_type').on('change',function(){
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
