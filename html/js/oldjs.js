var IE = document.all?true:false

var topLeftX = 0;  // these aren't nessesarily top/bottom or right/left... but it makes sense.
var topLeftY = 0;
var btmRightX = 0;
var btmRightY = 0;
var mouseDown=false;

function mapMouseDown() {	//mark first point
	mouseDown=true;
	container=document.getElementById('container');
	e=window.event;
	if (IE) {
		topLeftX = event.clientX + container.scrollLeft;
		topLeftY = event.clientY + container.scrollTop;
	} else {
		topLeftX = e.pageX - container.offsetLeft - 1;
		topLeftY = e.pageY - container.offsetTop - 1;
	}  

	document.getElementById('pushpin').style.display="block";
	document.getElementById('pushpin').style.left=topLeftX+"px";
	document.getElementById('pushpin').style.top=topLeftY+"px";
	document.getElementById('pushpin').style.height="2px";
	document.getElementById('pushpin').style.width="2px";
}


function mapMouseMove() { 		// click-and-drag functionality
	if (!mouseDown) {
		return;
	}
	container=document.getElementById('container');
	e=window.event;
	if (IE) {
		btmRightX = event.clientX + container.scrollLeft;
		btmRightY = event.clientY + container.scrollTop;
	} else {
		btmRightX = e.pageX - container.offsetLeft - 1;
		btmRightY = e.pageY - container.offsetTop - 1;
	}  

	document.getElementById('pushpin').style.display="block";
	document.getElementById('pushpin').style.left=Math.min(btmRightX,topLeftX)+"px";
	document.getElementById('pushpin').style.top=Math.min(btmRightY,topLeftY)+"px";
	document.getElementById('pushpin').style.height=Math.abs(btmRightY-topLeftY)+"px";
	document.getElementById('pushpin').style.width=Math.abs(btmRightX-topLeftX)+"px";
}


function mapMouseUp() {
	mouseDown=false;

//ajax request(s) go here...



}

