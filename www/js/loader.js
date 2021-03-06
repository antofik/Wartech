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
        script.src = 'js/' + scriptName + '.js';
        document.body.appendChild(script);
    }
}
