// $(document).ready(function(){
// 	$('body').on('click', function(){
// 		console.log('Logre linkear un archivo de JS a KASware!!! :)')
// 	});
// });


$('body').on('click', function(){
	console.log('Logre linkear un archivo de JS a KASware!!! :)')
});


function al_cargar(){
	console.log('mas o menos ahi va')
};
$(al_cargar);


$('#repeats').on('change',function(){
	if (this.value == 'R007'){
		$('#repeats_on').removeClass('hidden');
		console.log('Se repite cada semana');
	} else {
		$('#repeats_on').addClass('hidden');
	}
});