page = {};
var cache = {};
page.show = function(pageName){
    page.load(pageName, function(){

        $('.page')[0].className='page ' + pageName;
        $('.page').hide();
        $('.wait').show();

        page[pageName].init(function(){
            page[pageName].render(function(){
                $('.page').show();
                $('.wait').hide();
            });
        });
    });
}

page.load = function(pageName, callback){
    if (cache[pageName] !== undefined) {
        callback();
    }
    var url = 'js/page/' + pageName + '.js';
    $.ajax({
        url: url,
        success: function(reply){
            eval(reply);
            callback();
        }
    });
}
