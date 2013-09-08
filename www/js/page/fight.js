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
var interval = 1000;

var list = {};
var beginFight = function(fight){
    arena.init(fight.arena);
    $('title').html(fight.final_message);
    var tick = 0;
    var teams = [];
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
                            if (teams[val.team] == undefined) {
                                teams[val.team] = new Team();
                            }
                            list[val.name] = new Robot(val.name, teams[val.team]);
							break;
                        case 'dead':
                            break;
                        case 'removed':
                            var item = list[val.name];
                            item.remove();
                            delete list[val.name];
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
                    var t = arena.convertCoords(val.target_position[0], val.target_position[1]);
                    var startPosition = list[val.name].getShootCoords();
                    var s = new shoot(startPosition, [t[0]+15, t[1]+15]);
                    s.animateTick(interval / 2);
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
