var cache = [];
loader = {
    load: function(scriptName, callback){
        if (cache[scriptName] != undefined)
            return callback();

        var script = document.createElement('script');
        script.onload = function(){
            cache[url] = true;
            callback();
        }
        script.url = 'js/' + scriptName + '.js';
        $('body').appendChild(script);
    }
}
