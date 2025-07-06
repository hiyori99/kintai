from django import template

register = template.Library()

@register.filter
def timestring(value):
    try:
        seconds = int(value.total_seconds())
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        if hours > 0:
            return f"{hours}時間{minutes}分"
        return f"{minutes}分"
    except:
        return "0分"
