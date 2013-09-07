function robot(name)
{
    var healthWidth = 40;
    var that = this;
    this.drawWrap = function()
    {
        var wrap = svg.group(undefined, {
            width: that.width,
            height: that.height
        });
        var r1 = svg.rect(wrap, -20, -30, healthWidth, 4, {fill: 'red', strokeWidth: 0});
        var r2 = svg.rect(wrap, -20, -30, healthWidth, 4, {fill: 'green', strokeWidth: 0});
        $(r2).addClass('health');

        return wrap;
    }

    this.name = name;
    this.position = [];
    this.obj = null;
    this.objWrap = this.objWrap = this.drawWrap();;
    this.width = 100;
    this.height = 100;
    this.health = null;
    this.maxHealth = null;

    var currentDirection = 0;
    var oldDirection = 0;
    var oldPosition = 0;
    var oldAngle = 360;

    this.move = function(x, y)
    {
        that.position = arena.convertCoords(x, y);
    }

    this.rotate = function(direction)
    {
        currentDirection = that.direction;
        that.direction = direction;
    }

    this.animateTick = function(interval, callback)
    {
        oldPosition = oldPosition || that.position;
        var x = that.position[0] + 25;
        var y = that.position[1] + 18;

        var oldX = oldPosition[0] + 25;
        var oldY = oldPosition[1] + 18;

        var a = 360 - currentDirection * 60;
        if (Math.abs(a-oldAngle) > 180)
            a -= 360 * Math.round((a-oldAngle) / Math.abs(a-oldAngle));
        if (oldDirection == currentDirection) {
            $(that.obj).animate({
                svgTransform: 'rotate('+a+')'
            }, interval, 'linear');
            $(that.objWrap).animate({
                svgTransform: 'translate('+x+' '+y+')'
            }, interval, 'linear');
        } else {
            $(that.obj).animate({
                svgTransform: 'rotate('+a+')'
            }, 0.35 * interval, 'linear', function(){
                $(that.obj).animate({
                    svgTransform: 'rotate('+a+')'
                }, 0.65 * interval, 'linear');
                $(that.objWrap).animate({
                    svgTransform: 'translate('+x+' '+y+')'
                }, 0.65 * interval, 'linear');
            });
        }

        oldAngle = a;

        oldDirection = currentDirection;
        currentDirection = that.direction;
        oldPosition = that.position;
    }

    this.setHealth = function(health){
        that.health = health;
        that.maxHealth = that.maxHealth || health;
        $('.health', $(that.objWrap)).attr({width: healthWidth * health / that.maxHealth});
    }

    var draw = function()
    {
        var obj = svg.group(that.objWrap, {
            width: that.width,
            height: that.height
        });
        var rect = svg.rect(obj, -20, -15, 40, 30, {fill: '#fce', stroke: 'black'});
        var gun = svg.rect(obj, 20, -1, 30, 1, {fill: '#fce', stroke: 'black'});

        var robotDebug = $('.debug .robotPoint');
        $(obj).hover(function(){
            robotDebug.html(that.position[0] + ', ' + that.position[1] + ': ' + that.direction);
        }, function(){
            robotDebug.html('');
        });


        return obj;
    }

    this.getShootCoords = function()
    {
        return this.position;
    }



    this.obj = draw();

}




