function shoot(startPosition, endPosition)
{
    console.log(startPosition, endPosition);
    var width = 30;
    var height = 30;
    var that = this;

    this.draw = function()
    {
        var obj = svg.group(this.objWrap, {
            width: width,
            height: height
        });

        svg.circle(obj, 0, 0, 5, {stroke: '#ccc', strokeWidth: 1, fill: 'grey'});

        return obj;
    }

    this.drawWrap = function()
    {
        var obj = svg.group(undefined, {
            width: width,
            height: height
        });

        $(obj).animate({svgTransform: 'translate(-1000 -1000)'});

        return obj;
    }

    this.animateTick = function(interval)
    {
        var x = startPosition[0];
        var y = startPosition[1];
        $(that.objWrap).animate({
            svgTransform: 'translate('+x+' '+y+')'
        }, 0, function(){
            var x = endPosition[0];
            var y = endPosition[1];
            $(that.objWrap).animate({
                svgTransform: 'translate('+x+' '+y+')'
            }, interval, function(){
                $(that.objWrap).remove();
            });
        });
    }

    this.objWrap = this.drawWrap();
    this.obj = this.draw();
}