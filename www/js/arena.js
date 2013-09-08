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
            var group = svg.group('arena');
            var defs = svg.defs(group);
            var pattern = svg.pattern(defs, 'grass', 0, 0, 60, 68);
            var grass = svg.image(pattern, 0, 0, 60, 68, 'img/arena/grass.jpg');
            var pattern = svg.pattern(defs, 'water', 0, 0, 60, 68);
            var grass = svg.image(pattern, 0, 0, 60, 68, 'img/arena/water.gif');

			var currentLocation = $('.debug .currentPoint');
            var index = _arena.width * _arena.height - 1;
			for (var i = 0; i < _arena.width; i++){
				for (var j = -Math.floor(i/2); j < _arena.height - Math.floor(i/2); j++){
					var c = arena.convertCoords(j, i);
					var p = drawGexoid(group, 30, c, _arena.terrain[index]);
					(function(){
						var text = j + ', ' + i;
						p.hover(function(){
							currentLocation.html(text);
						}, function(){
							currentLocation.html();
						});
					})();
                    index--;
				}
			}
		}
	});
}

arena.convertCoords = function(x, y){
	return [(y/2+x) * config.cellSize * Math.sqrt(3), height - 1.5 * (y+1) * config.cellSize];
}


var drawGexoid  = function(group, l, point, index){
	var points = [point];

    var patterns = [
        'none', 'brown'
    ];

	for (var i = 1; i < 6; i++) {
		var a = (i+3) * Math.PI / 3 + Math.PI/2;
		points.push([
			Math.round(points[i-1][0] + l * Math.cos(a)),
			Math.round(points[i-1][1] + l * Math.sin(a))
		]);
	}
	var p = $(svg.polygon(group, points, {
        stroke: '#eee',
        strokeWidth: 1,
        fill: patterns[index]
    }));

	p.addClass('cell');


	//svg.circle(point[0], point[1], 1);

	return p;
}