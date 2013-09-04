window.template = {};

window.template.load = function(url, callback) {
    $.get('template/' + url + '.html', {}, callback);
};
