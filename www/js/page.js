page = {};
page.configurator = {}
page.configurator.render = function(){
    api.init(function(){
        api.isAuthorized(function(isAuthorized){
            if (isAuthorized) {
                robot.init(function(robot){
                    page.configurator.show();
                });
            } else {
                auth.tryAuthorize(function(isAuthorized){
                    $('.__auth-url').show();
                    alert('Вам необходимо авторизироваться');
                })
            }
        })
    });

}

page.configurator.show = function(){
    $('.wait').hide();
    $('.page').show();
}