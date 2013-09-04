api = {};

api.init = function(callback) {
    return callback();
};

api.request = function(method, data, callback) {
    callback = callback || console.log;
    data = data || {}
    url = 'http://logic.wartech.pro/' + method;
    data.sessionid = $.cookie('sessionid')
    $.getJSON(url, data, function(reply) {
		callback(reply);
	});
};

api.getAllUsers = function(callback) {
    return api.request('get_all_users', {}, callback);
};

api.requestFight = function(fight_with, callback) {
    return api.request('request_fight', {
        fight_with: fight_with
    }, callback);
};

api.getAllModules = function(callback) {
    return api.request('get_all_modules', {}, callback);
};

api.getUserRobot = function(callback) {
    return api.request('get_user_robot', {}, callback);
};

api.getUserModules = function(callback) {
    return api.request('get_user_modules', {}, callback);
};

api.setModuleToSlot = function(slot_id, module_id, callback) {
    return api.request('set_module_to_slot', {
        slot_id: slot_id,
        module_id: module_id
    }, callback);
};

api.isAuthorized = function(callback) {
    return api.request('is_authorized', {}, callback);
};

api.login = function(token, provider, callback) {
    return api.request('login', {
        token: token,
        provider: provider
    }, callback);
};

api.testFight = function(callback){
    return api.request('test_fight', {}, callback);
}

api.requestFight = function(callback){
    return api.request('request_fight', {}, callback);
}
