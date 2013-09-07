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
var tickInterval = 500;
var interval = 500;

var list = {};
var beginFight = function(fight){
    arena.init(fight.arena);
    $('title').html(fight.final_message);
    var tick = 0;
	var processTick = function(){
		var data = fight.journal[tick];
		//console.log(data);
		for (i in data) {
			var val = data[i];
			type = val.type;
			var wrap = arena.wrap;
			switch (type) {
				case 'general':
					switch (val.action){
						case 'start':
                            list[val.name] = new robot(val.name);
							break;
                        default:
                            console.log('Unknown action: ', val.action, val);
                            break;
					}
					break;
				case 'health':
					list[val.name].setHealth(val.value);
					break;
				case 'start_position':
					var item = list[val.name];
                    item.move(val.x, val.y);
					break;
				case 'move':
                    var item = list[val.name];
                    item.move(val.x, val.y);
					break;
				case 'start_direction':
				case 'turn':
                    var item = list[val.name];
                    item.direction = val.direction;
					break;
                case 'shoots':
                    var targetPosition = arena.convertCoords(val.target_position[0], val.target_position[1]);
                    var startPosition = list[val.name].getShootCoords();
                    var s = new shoot(startPosition, targetPosition);
                    s.animateTick(interval);
                    break;
                default:
                    console.log('Unknown type: ', type, val);
                    break;
			}
		}
        for (i in list)
            list[i].animateTick(interval);
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
