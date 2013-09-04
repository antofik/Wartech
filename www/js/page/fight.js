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

var beginFight = function(fight){
    arena.init(fight.arena);
    $('title').html(fight.final_message);
    var list = {};
    var tick = 0;
    var interval = 100;
    setInterval(function(){
        var data = fight.journal[tick];
        for (i in data) {
            var val = data[i];
            type = val.type;
            var wrap = arena.wrap;
            switch (type) {
                case 'general':
                    switch (val.action){
                        case 'start':
                            var obj = {};
                            var html = '<div class="arena-object">' +
                                            '<div class="health">-</div>' +
                                            '<div class="name">' + val.name + '</div>' +
                                        '</div>';
                            $(wrap).append(html);
                            obj.obj = $('.arena-object:last', wrap);
                            list[val.name] = obj;
                        break;
                    }
                    break;
                case 'health':
                    list[val.name].health = val.value;
                    setTimeout(function(){
                        $('.name', list[val.name].obj).html(val.value);
                    }, interval);
                    break;
                case 'start_position':
                    var item = list[val.name];
                    item.x = val.x;
                    item.y = val.y;
                    var c = arena.convertCoords(item.x, item.y);
                    list[val.name].obj.css({
                        left: c[0] + 'px',
                        top: c[1] + 'px'
                    });
                    break;
                case 'move':
                    var item = list[val.name];
                    console.log(item.y, item.x);
                    var c = arena.convertCoords(item.x, item.y);
                    item.x = val.x;
                    item.y = val.y;
                    list[val.name].obj.animate({
                        left: c[0] + 'px',
                        top: c[1] + 'px'
                    }, interval);
                    break;
            }

        }
        tick++;
    }, interval);
}