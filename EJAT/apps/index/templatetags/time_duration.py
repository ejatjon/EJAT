import datetime

from django import template

register = template.Library()


@register.filter(name="time_duration")
def time_duration(value):
    try:
        data=[int(i) for i in value.split(" ")[0].split("-")]
        data=data+[eval(i) for i in value.split(" ")[1].split(":")]
        Y, M, d, H, m, s, = data[0],data[1],data[2],data[3],data[4],int(data[5]//5)
        data = datetime.datetime(year=Y,month=M,day=d,hour=H,minute=m,second=s)
        now = datetime.datetime.now()
        duration = now - data
        if duration.days > 365:
            return "%d Years ago" % (duration.days // 365)
        if duration.days > 30:
            return "%d Month ago" % (duration.days // 30)
        if duration.days >= 7:
            return "%d Weeks ago" % (duration.days // 7)
        if 7 > duration.days >= 1:
            return "%d Days ago" % duration.days
        if duration.seconds >= 60*60:
            return "%d Hours ago" % (duration.seconds // 60*60)
        if duration.seconds >= 60:
            return "%d Minutes ago" % (duration.seconds // 60)
        else:
            return "%d Seconds ago" % duration.seconds
    except Exception:
        return "Time unknown"

