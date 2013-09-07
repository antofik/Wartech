arena = {}
var config = {
    cellSize: 30
}
var width, height;

arena.init = function(_arena){
    var wrap = arena.wrap = $('#arena');
    width = _arena.width * config.cellSize * Math.sqrt(3);
    height = _arena.height * config.cellSize * 1.5 + config.cellSize/2;
    wrap.css({
        width: width + 'px',
        height: height + 'px'
    });

	$('#arena').svg({
		onLoad: function(svg){
			window.svg = svg;

			var arenaWidth = 8;
			var arenaHeight = 8;

			var currentLocation = $('.debug .currentPoint');
			for (var i = 0; i < arenaWidth; i++){
				for (var j = -Math.floor(i/2); j < arenaHeight - Math.floor(i/2); j++){
					var c = arena.convertCoords(j, i);
					var p = drawGexoid(30, c);
					(function(){
						var text = j + ', ' + i;
						p.hover(function(){
							currentLocation.html(text);
						}, function(){
							currentLocation.html();
						});
					})();
				}
			}
		}
	});
}

arena.convertCoords = function(x, y){
	return [(y/2+x) * config.cellSize * Math.sqrt(3), height - 1.5 * (y+1) * config.cellSize];
}


var drawGexoid  = function(l, point){
	var points = [point];

	for (var i = 1; i < 6; i++) {
		var a = (i+3) * Math.PI / 3 + Math.PI/2;
		points.push([
			Math.round(points[i-1][0] + l * Math.cos(a)),
			Math.round(points[i-1][1] + l * Math.sin(a))
		]);
	}
	var p = $(svg.polygon(points, {stroke: '#eee', strokeWidth: 1, fill: 'transparent'}));
	p.addClass('cell');

	//svg.circle(point[0], point[1], 1);

	return p;
}