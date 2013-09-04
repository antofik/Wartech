page = {};
var cache = {};
page.show = function(pageName){
    page.load(pageName, function(){

        $('.page')[0].className='page ' + pageName;
        $('.page').hide().html('');
        $('.wait').show();
        $('title').html('Загрузка страницы...');
        var config = page[pageName].config || {};

        var show = function(){
            $('title').html(config.title || pageName);
            page[pageName].init(function(){
                page[pageName].render(function(){
                    $('.page').show();
                    $('.wait').hide();
                });
            });
        }

        if (config.onlyLogined) {
            api.isAuthorized(function(isAuthorized){
                if (isAuthorized) {
                    show();
                } else {
                    auth.tryAuthorize(function(isAuthorized){
                        page.show('login');
                    })
                }
            })
        } else{
            show();
        }


    });
}

page.load = function(pageName, callback){
    if (cache[pageName] !== undefined) {
        callback();
    }
    var url = 'js/page/' + pageName + '.js';
    $.ajax({
        url: url,
        dataType: 'html',
        success: function(reply){
            eval(reply);
            cache[pageName] = true;
            callback();
        }
    });
}
