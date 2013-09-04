page = {};
var cache = {};
page.show = function(pageName){
    page.load(pageName, function(){
        page.call(pageName);
    });
}

page.load = function(pageName){

}
