window.robot = {};

robot.init = function(callback) {
    var count = 3;
    var c = function(){
        count--;
        if (count == 0) {
            url = 'hull/' + robot[0].hull.name;
            template.load(url, function(reply){
                $('.hull').html(reply).addClass(robot.hull_name);
                callback(robot);
            });
        }
    }
    var robot = null, userModules = null, robotModules = null;
    api.getUserRobot(function(_robot){
        robot = _robot;
        c();
    });
    api.getUserModules(function(_userModules){
        userModules = _userModules;
        c();
    });
    api.getAllModules(function(_allModules){
        allModules = _allModules;
        c();
    });
};

robot.getDressed = function() {

};
