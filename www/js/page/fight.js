page.fight = {
    config: {
        onlyLogined: true,
        title: 'Бой'
    }
}

var initialized = false;


page.fight.init = function(callback){
    if (initialized)
        return callback();

    callback();
}

page.fight.render = function(callback){
    var count = 3;
    var fight;
    var c = function(){
        count--;
        if (count == 0) {
            beginFight(fight);
            callback();
        }
    }
    api.testFight(function(_fight){
        fight = _fight;
        c();
    });
    loader.load('arena', c);

    template.load('page/fight', function(html){
        $('.page').html(html);
        c();
    });
}
var tickInterval = 1000;
var interval = 200;

var list = {};
var beginFight = function(fight){
    arena.init(fight.arena);
    $('title').html(fight.final_message);
    var tick = 0;
	var processTick = function(){
		var data = fight.journal[tick];
		console.log(data);
		for (i in data) {
			var val = data[i];
			type = val.type;
			var wrap = arena.wrap;
			var robotDebug = $('.debug .robotPoint');
			switch (type) {
				case 'general':
					switch (val.action){
						case 'start':
                            list[val.name] = new robot(val.name);
							break;
					}
					break;
				case 'health':
					//list[val.name].health = val.value;
					//list[val.name].obj.animate({svgTransform: 'opacity('+val.value / 100+')'}, 0);
					break;
				case 'start_position':
					var item = list[val.name];
                    item.move(val.x, val.y);
					break;
				case 'move':
                    var item = list[val.name];
                    item.move(val.x, val.y);
                    item.animateTick(interval);
					break;
				case 'turn':
                    var item = list[val.name];
                    item.rotate(val.direction);
                    item.animateTick(interval);
					break;
			}

		}
		tick++;
	};


	var processTickWrapped = function(){
		setTimeout(processTickWrapped, tickInterval);
		if ($('#pause:checked').length > 0)
			return;
		processTick();
	}

	processTickWrapped();
	$('.next-tick').click(function(){
		processTick();
	});

}
var animateRobot = function(_robot)
{
	var transform = [];
	var x = _robot.position[0] + Math.cos(26 * _robot.direction * Math.PI/3);
	var y = _robot.position[1] - Math.sin(26 * _robot.direction * Math.PI/3);
	transform.push('translate('+x+', '+y+')');
	transform.push('rotate('+(_robot.direction * 60)+')');
	$(_robot.obj).animate({svgTransform: transform.join(' ')}, interval);
}

var drawRobot = function(point){
	var s = 20;
	//var points = [point, [point[0]+s, point[1]-s], [point[0]+s+s, point[1]], [point[0]+s, point[1]+s]];
	var x = point[0] + 15;
	var y = point[1] + 15;
	var points = [[x, y-15], [x+30, y], [x, y+15]];
	return svg.polygon(points, {stroke: 'blue', fill: 'red'});
}

window.moveRobot = function(name, x, y, direction)
{
	if (name == null)
		for (i in list) {
			name = i;
			break;
		}

	var item = list[name];
	var c = arena.convertCoords(item.x, item.y);
	item.x = x;
	item.y = y;
	item.position = c;
	item.direction = direction;
	animateRobot(item);
}