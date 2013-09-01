window.api = {};

api.init = (callback) ->
  $.ajaxSetup({
    xhrFields: {
      withCredentials: true
    },
    crossDomain: true
  });
  callback();

window.api.request = (method, data, callback) ->
    url = 'http://logic.wartech.pro/' + method;
    await $.getJSON url, data, defer reply
    callback(reply);

window.api.getAllUsers = (callback) ->
    api.request('get_all_users', {}, callback);

window.api.requestFight = (fight_with, callback) ->
    api.request('request_fight', {fight_with: fight_with}, callback);

window.api.getAllModules = (callback) ->
    api.request('get_all_modules', {}, callback);

window.api.getUserRobot = (callback) ->
    api.request('get_user_robot', {}, callback);

window.api.getUserModules = (callback) ->
   api.request('get_user_modules', {}, callback);

window.api.setModuleToSlot = (slot_id, module_id, callback) ->
    api.request('set_module_to_slot', {
        slot_id: slot_id,
        module_id: module_id
    }, callback)

window.api.isAuthorized = (callback) ->
    api.request('is_authorized', {}, callback)



window.api.login = (token, provider, callback) ->
    api.request('login', {
        token: token,
        provider: provider
    }, callback)


