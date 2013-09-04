auth = {};

auth.login = function() {
  var redirect_uri;
  redirect_uri = 'http://wartech.pro/oauth.php?adapter=vk.com&domain=' + location.host;
  return document.location = 'https://oauth.vk.com/authorize?client_id=3851736&scope=PERMISSIONS&redirect_uri=' + encodeURIComponent(redirect_uri) + '&response_type=code&v=5.0';
};

auth.tryAuthorize = function(callback)
{
    if (matches = document.location.toString().match(/&code=(\w+)/)) {
        api.login(matches[1], 'vk', function(reply){
            $.cookie('sessionid', reply.sessionid);
            location = '/configure.html';
            callback(true);
        });
    } else {
        callback(false);
    }
}
