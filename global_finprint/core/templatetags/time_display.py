from math import floor
from django import template
register = template.Library()


def time_display(pos):
    s, m = divmod(floor(pos), 1000)
    h, s = divmod(s, 60)
    return "{0:02}:{1:02}:{2:03}".format(h, s, m)


register.filter('time_display', time_display)
