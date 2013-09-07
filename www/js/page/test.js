page.test = {}

page.test.init = function(calback){
	calback();
}

page.test.render = function(callback){
	template.load('page/test', function(html){
		$('.page').html(html);
		$('#arena').svg({
			onLoad: function(svg){
				window.svg = svg;




				var arenaWidth = 8;
				var arenaHeight = 8;
				for (var i = 0; i < arenaWidth; i++){
					for (var j = -Math.floor(i/2); j < arenaHeight - Math.floor(i/2); j++){
						var c = convertCoords(j, i);
						gex(30, c);
					}
				}

				/*var l = 30;
				gex(l, [0, l]);
				gex(l, [l * Math.sqrt(3), l]);*/

				/*svg.circle(75, 75, 50, {fill: 'none', stroke: 'red', 'stroke-width': 3});
				var g = svg.group({stroke: 'black', 'stroke-width': 2});
				svg.line(g, 15, 75, 135, 75);
				svg.line(g, 75, 15, 75, 135);*/
		}});
		callback();
	});
}

var convertCoords = function(x, y){
	return [(y/2+x) * 30 * Math.sqrt(3), 400 - 1.5 * y * 30];
}
