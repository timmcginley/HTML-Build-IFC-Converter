// ok in here we need to include a lot of stuff.
// we need a menu... where would this fit?
// we need to start (over)loading stuff into the DOM.
// we need to split the screen into section and plan and KPIs and info - where should this go?


function main() {
	const floors = document.getElementsByTagName("floor-");
	let num_floors = floors.length;
	console.log(num_floors);
	$('project-').prepend('number of floors is '+num_floors);
	$('project-').prepend('\nsite elevation is '+$('site-').attr('elev'));
}


/*
var container = document.getElementById('pcontainer');
container.insertBefore(document.createElement("p"), container.firstChild);

*/

// <project-> - title etc.... | <site-> - also menu? site specific data?
// ---------------------------------------------------------------------
// <building-> - name of the building? this then needs to split in two...
// could also be more views and show a 3d? but maybe left is consistent
// ---------------------------------------------------------------------
// #section                   |               #plan
// this shows the floors      |      this shows a floor in plan         |
// in section                 |                 #plan                   |
//    <floor...->              -----------------------------------------
//                            |                 <properties->           |
// ---------------------------------------------------------------------