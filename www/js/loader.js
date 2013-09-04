var cache = [];
loader = {

}
loader.load = function(scriptName, callback){
    if (cache[scriptName] != undefined)
        return callback();

    $.ajax({
        url: 'js/' + scriptName + '.js',
        dataType: 'html',
        success: function(reply){
            eval(reply);
            cache[url] = true;
            callback();
        }
    });
}
