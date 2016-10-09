var picno = 0;
function change(){
	var image=document.getElementById('ss');
	if(picno==3) {
		image.innerHTML=Array[0];
		picno=0;
	} else if(picno<3) {
		image.innerHTML=Array[++picno];
	}
	timer = setTimeout(change, 2000);
}
var Array = ["Your Kitchen Chaperon !!!","Let us inspire you!","Discover, save and share best recipes!","Cooking fun @Your Kitchen Chaperon"];
