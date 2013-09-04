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
    template.load('page/fight', function(html){
        $('.page').html(html);
        callback();
    });
}