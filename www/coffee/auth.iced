window.auth = {}
auth.login = () ->
    redirect_uri = 'http://wartech.pro/oauth.php?adapter=vk.com&domain=' + location.host;
    document.location = 'https://oauth.vk.com/authorize?client_id=3851736&scope=PERMISSIONS&redirect_uri=' + encodeURIComponent(redirect_uri) + '&response_type=code&v=5.0';
