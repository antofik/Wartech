window.robot = {};


robot.init = (callback) ->
    await api.getUserRobot defer _robot
    await api.getAllModules defer robot.allModules
    await api.getUserModules defer robot.userModules

    $.extend(robot, _robot);
    url = 'hull/' + robot.hull_name;
    await template.load url, defer reply
    $('.hull').html(reply).addClass(robot.hull_name);
    callback(robot);

robot.getDressed = () ->
    for module in robot.userModules
        if (!module.equipped)
           return;
