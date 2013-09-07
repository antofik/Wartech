function robot(name)
{
    this.name = name;
    this.position = [];
    this.obj = null;
    this.width = 100;
    this.height = 100;

    this.move = function(x, y)
    {
        this.position = arena.convertCoords(x, y);
    }

    this.rotate = function(direction)
    {
        this.direction = direction;
    }

    this.animateTick = function(interval, callback)
    {
        var x = this.position[0] + 25;
        var y = this.position[1] + 18;
        $(this.obj).animate({
            svgTransform: 'translate('+x+' '+y+') rotate('+(this.direction * 60)+')'
        }, interval);
    }

    var draw = function()
    {
        var that = this;
        var obj = svg.group(undefined, {
            width: this.width,
            height: this.height
        });
        var rect = svg.rect(obj, -20, -15, 40, 30, {fill: '#fce', stroke: 'black'});
        var gun = svg.rect(obj, 20, -1, 30, 1, {fill: '#fce', stroke: 'black'});

        $(obj).hover(function(){
            robotDebug.html(that.position[0] + ', ' + that.position[1] + ': ' + that.direction);
        }, function(){
            robotDebug.html('');
        });

        return obj;
    }


    this.obj = draw();
}



