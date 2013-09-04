page.configurator = {
    config: {
        onlyLogined: true,
        title: 'Конфигуратор'
    }
}

var initialized = false;

page.configurator.init = function(callback){
    if (initialized)
        return callback();

    robot.init(function(robot){
        initialized = true;
        callback();
    });
}

page.configurator.render = function(onRendered){
    onRendered();
}

