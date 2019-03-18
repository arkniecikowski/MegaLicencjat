
var listaCheckow = [];

function CheckBoxClick(x) {

	var headerSecondDiv = document.getElementsByClassName('headerSecond')[0];

	if(listaCheckow.includes(x)){
		listaCheckow =  listaCheckow.filter(function(item) {
			return item !== x;
		});
		} else {
			listaCheckow.push(x);
		}

	if (listaCheckow.length>0){
			headerSecondDiv.style.display = 'block';
		} else {
			headerSecondDiv.style.display = 'none';
		}


	$('#btnRename').click(function() {
		if(listaCheckow.length==1) {
			var modalRename = document.getElementById('modalRename');
			modalRename.style.display = 'block';
			zamknij(modalRename);
		}
	});
}

function zamknij(modal) {
	var closeBtn = document.getElementsByClassName('closeBtn')[0];

	closeBtn.addEventListener('click',closeModal);
	window.addEventListener('click', cliclOutSide);

	function closeModal() {
			modal.style.display = 'none';
			}
	function cliclOutSide(e) {
		if (e.target == modal) {
			modal.style.display = 'none';
		}
	}
}


function ZmienLokacje(x) {
	window.location = x;
}

$(document).ready(function(){
	$('#buttonUpload').click(function(){
  		$('#fileUpload').click();
  		var modalDodajPlik = document.getElementById('modalDodajPlik');
  		modalDodajPlik.style.display = 'block';
  		zamknij(modalDodajPlik);
	  });
	});

$(document).ready(function(){
	$('#modelCheckButton').click(function () {
	var modalNowyFolder = document.getElementById('modalNowyFolder');
	modalNowyFolder.style.display = 'block';
	zamknij(modalNowyFolder);
	});
});
