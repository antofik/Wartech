page.configurator = {}
var initialized = false;

page.configurator.init = function(callback){
    if (initialized)
        return callback();

    api.init(function(){
        api.isAuthorized(function(isAuthorized){
            if (isAuthorized) {
                robot.init(function(robot){
                    initialized = true;
                    callback();
                });
            } else {
                auth.tryAuthorize(function(isAuthorized){
                    page.show('login');
                })
            }
        })
    });
}

page.configurator.render = function(onRendered){
    onRendered();
}

