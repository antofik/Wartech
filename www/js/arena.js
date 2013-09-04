arena = {}
var config = {
    cellSize: [60, 45]
}
var width, height;

arena.init = function(_arena){
    var wrap = arena.wrap = $('.arena');
    width = _arena.width * config.cellSize[0];
    height = _arena.height * config.cellSize[1];
    wrap.css({
        width: width + 'px',
        height: height + 'px'
    });

    for (var i = 0; i < 8; i++){
        for (var j = -Math.floor(i/2); j < 8 - Math.floor(i/2); j++){
            var c = arena.convertCoords(j, i);
            x = c[0] + 20;
            y = c[1] - 40;
            var html = '<div class="coords" style="left: ' + x + 'px; top: ' + y + 'px;">' + j + ' ' + i + '</div>';
            wrap.append(html);
        }
    }
}

arena.convertCoords = function(x, y){
    return [(y/2+x) * config.cellSize[0], height - y * config.cellSize[1]];
}

