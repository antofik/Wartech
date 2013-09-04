page.login = {}

page.login.init = function(calback){
    calback();
}

page.login.render = function(callback){
    template.load('page/login', function(html){
        $('.page').html(html);
        callback();
    });
}